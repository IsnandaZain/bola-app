# bola-app

Aplikasi ini merupakan aplikasi tentang sepakbola yang mencakup beberapa entitas seperti pemain (player), tim dan liga.

This Project Setup :

DATABASE (Environment) :
- DB_NAME (Nama dari Database) - default: soccer
- DB_USER (User dari akun mysql) - default: root
- DB_PASS (Pass user dari akun mysql) - default: -
- DB_HOST (Host dari Database) - default: 127.0.0.1

INSTALL PACKAGES :
pip install -r requirements.txt

RUN PROJECT:
uwsgi --module soccer.http --callable app --enable-threads --master --processes 2

*if fail, add --http :5000 , after run project command (to run project in port 5000)

