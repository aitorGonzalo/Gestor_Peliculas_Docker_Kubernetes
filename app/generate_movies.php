<?php
require 'vendor/autoload.php'; 
use Faker\Factory;
sleep(40);

$faker = Factory::create();

// Géneros predefinidos
$genres = ["Action", "Drama", "Comedy", "Thriller", "Sci-Fi", "Horror", "Romance", "Adventure"];

// URL del servicio Flask
$flask_url = getenv('FLASK_SERVICE_URL') . '/add_movie';

function generate_movie() {
    global $faker, $genres;

    return [
        "title" => $faker->sentence(3),  
        "type" => $faker->randomElement(["Movie", "Series"]),  
        "genres" => implode(", ", $faker->randomElements($genres, rand(1, 3))),  
        "release_year" => $faker->year,  
        "imdb_id" => $faker->unique()->regexify('tt[0-9]{7}'),  
        "imdb_average_rating" => $faker->randomFloat(1, 1, 10),  
        "imdb_num_votes" => $faker->numberBetween(1, 1000000),  
        "available_countries" => implode(", ", $faker->randomElements(["US", "UK", "FR", "DE", "IN", "JP", "ES", "IT"], rand(1, 5)))  // Países disponibles
    ];
}

// Función para enviar datos al servicio Flask
function send_movie($movie) {
    global $flask_url;

    $ch = curl_init($flask_url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($movie));

    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($http_code === 201) {
        echo "Película añadida: " . $movie['title'] . "\n";
    } else {
        echo "Error al añadir película: $http_code\n";
        echo "Respuesta: $response\n";
    }
}

// Bucle infinito para generar y enviar películas cada minuto
while (true) {
    $movie = generate_movie();
    print_r($movie); 
    send_movie($movie);
    sleep(60); 
}
