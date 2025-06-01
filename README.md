Tubes1_Skibidi       LINK YOUTUBE : https://youtu.be/AC98ZJM4ghM
📋 Deskripsi
Tugas Besar 1 - Strategi Algoritma yang mengimplementasikan algoritma greedy untuk menyelesaikan permasalahan optimasi. Proyek ini menggunakan pendekatan greedy untuk mencari solusi optimal lokal dalam setiap langkah dengan harapan mencapai solusi optimal global.
👥 Anggota Kelompok

M. Daffa Hakim Matondang - NIM: 123140002
Febrian Valentino Nugroho - NIM: 123140034
Ola Anggela Rosita - NIM: 123140042


Konsep Dasar
Algoritma greedy adalah paradigma algoritma yang membuat pilihan optimal lokal pada setiap langkah dengan harapan menemukan optimum global. Algoritma ini bekerja dengan prinsip:

Greedy Choice: Selalu memilih pilihan terbaik yang tersedia saat ini
Optimal Substructure: Solusi optimal mengandung solusi optimal dari submasalah
No Backtracking: Tidak pernah mengubah keputusan yang sudah dibuat

Implementasi dalam Proyek
Proyek ini mengimplementasikan algoritma greedy untuk optimasi pergerakan bot dalam game diamond collection. Bot menggunakan strategi greedy untuk memilih target diamond dan rute pergerakan yang optimal.
Lokasi Implementasi Greedy:

Pemilihan Target Diamond (search_optimal method)

Greedy by: Rasio nilai diamond terhadap jarak (points/distance)
Fungsi evaluasi: evaluation = (total_points/(total_distance + last_goal_to_base))
Bot selalu memilih kombinasi diamond yang memberikan rasio nilai tertinggi per jarak tempuh


Pemilihan Arah Gerak (get_direction method)

Greedy by: Jarak Euclidean terpendek ke target
Kriteria: euclidean = sqrt((new_x - dest.x)**2 + (new_y - dest.y)**2)
Bot selalu bergerak ke arah yang mengurangi jarak ke target secara maksimal


Pemilihan Rute Teleport (distance method)

Greedy by: Jarak Manhattan terpendek (dengan/tanpa teleport)
Kriteria: Membandingkan jarak langsung vs melalui teleport, pilih yang terpendek
Bot selalu memilih rute dengan total jarak minimum


Strategi Combat (_handle_combat method)

Greedy by: Prioritas waktu tersisa (milliseconds_left)
Bot menyerang lawan yang memiliki waktu tersisa lebih sedikit

//CARA BUKA PATH FILE BOT NYA DI CMD 
Yaitu jika windows kalian jangan lupa masuk ke file explorer lalu masuk ke folder Tubes1_Skibidi klik klik sampe ke folder src jika sudah sampai di folder src barulah kalian masukkan pemanggilan botnya
cth:
start cmd /c "python main.py --logic Sifu --email=test2@email.com --name=stima2 --password=123458 --team etimo"
start cmd /c "python main.py --logic Sifu --email=test40@email.com --name=stima4 --password=123460 --team etimo"
start cmd /c "python main.py --logic Master --email=test4394@email.com --name=stima13 --password=123460 --team etimo"
start cmd /c "python main.py --logic Master --email=test420@email.com --name=stima6 --password=123460 --team etimo"
enter di CMD. SELAMAT MENCOBAA


//GAME ENGINE BY ETIMO DIAMONDS
//CARA RUN PROGRAM SESUAI SPEK TUBES 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# 💎 Etimo Diamonds 2

Diamonds is a programming challenge. Program a bot and compete to get the highest score. For more information:

-   [Project Specification](https://docs.google.com/document/d/13cbmMVXviyu8eKQ6heqgDzt4JNNMeAZO/edit)
-   [Get Started with Diamonds](https://docs.google.com/document/d/1L92Axb89yIkom0b24D350Z1QAr8rujvHof7-kXRAp7c/edit)

## Installing Dependencies 🔨

1. Clone this repository and move to the root of this project's directory

    ```
    git clone https://github.com/haziqam/tubes1-IF2110-bot-starter-pack.git
    cd ./tubes1-IF2110-bot-starter-pack
    ```

2. Install dependencies

    ```
    pip install -r requirements.txt
    ```

## How to Run 💻

1. To run one bot

    ```
    python main.py --logic Random --email=your_email@example.com --name=your_name --password=your_password --team etimo
    ```

2. To run multiple bots simultaneously

    For Windows

    ```
    ./run-bots.bat
    ```

    For Linux / (possibly) macOS

    ```
    ./run-bots.sh
    ```

    <b>Before executing the script, make sure to change the permission of the shell script to enable executing the script (for linux/macOS)</b>

    ```
    chmod +x run-bots.sh
    ```

#### Note:

-   If you run multiple bots, make sure each emails and names are unique
-   The email could be anything as long as it follows a correct email syntax
-   The name, and password could be anything without any space

## Credits 🪙

This repository is adapted from https://github.com/Etimo/diamonds2

Some code in this repository is adjusted to fix some issues in the original repository and to adapt to the requirements of Algorithm Strategies course (IF2211), Informatics Undergraduate Program, ITB.

©️ All rights and credits reserved to [Etimo](https://github.com/Etimo)
