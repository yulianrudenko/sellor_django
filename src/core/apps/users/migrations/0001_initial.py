# Generated by Django 3.2 on 2022-09-25 13:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

CITIES = [
	'Aleksandrów Kujawski', 'Aleksandrów Łódzki', 'Alwernia', 'Andrychów', 'Annopol', 'Augustów', 'Babimost', 'Baborów', 'Baranów Sandomierski', 'Barcin', 'Barczewo', 'Bardo', 'Barlinek', 'Bartoszyce', 'Barwice', 'Bełchatów', 'Bełżyce', 'Biała', 'Biała Piska', 'Biała Podlaska', 'Biała Rawska', 'Białobrzegi', 'Białogard', 'Biały Bór', 'Białystok', 'Biecz', 'Bielawa', 'Bielsk Podlaski', 'Bielsko-Biała', 'Bierutów', 'Bieruń', 'Bieżuń', 'Biskupiec', 'Bisztynek', 'Biłgoraj', 'Blachownia', 'Bobolice', 'Bobowa', 'Bochnia', 'Bodzentyn', 'Bogatynia', 'Boguchwała', 'Boguszów-Gorce', 'Bojanowo', 'Bolesławiec', 'Bolków', 'Borek Wielkopolski', 'Borne Sulinowo', 'Braniewo', 'Brańsk', 'Brodnica', 'Brok', 'Brusy', 'Brwinów', 'Brzeg', 'Brzeg Dolny', 'Brzesko', 'Brzeszcze', 'Brzeziny', 'Brześć Kujawski', 'Brzostek', 'Brzozów', 'Budzyń', 'Buk', 'Bukowno', 'Busko-Zdrój', 'Bychawa', 'Byczyna', 'Bydgoszcz', 'Bystrzyca Kłodzka', 'Bytom', 'Bytom Odrzański', 'Bytów', 'Będzin', 'Błaszki', 'Błażowa', 'Błonie', 'Cedynia', 'Chełm', 'Chełmek', 'Chełmno', 'Chełmża', 'Chmielnik', 'Chocianów', 'Chociwel', 'Chocz', 'Chodecz', 'Chodzież', 'Chojna', 'Chojnice', 'Chojnów', 'Choroszcz', 'Chorzele', 'Chorzów', 'Choszczno', 'Chrzanów', 'Chęciny', 'Ciechanowiec', 'Ciechanów', 'Ciechocinek', 'Cieszanów', 'Cieszyn', 'Ciężkowice', 'Cybinka', 'Czaplinek', 'Czarna Białostocka', 'Czarna Woda', 'Czarne', 'Czarnków', 'Czchów', 'Czechowice-Dziedzice', 'Czeladź', 'Czempiń', 'Czerniejewo', 'Czersk', 'Czerwieńsk', 'Czerwionka-Leszczyny', 'Czerwińsk nad Wisłą', 'Czyżew', 'Częstochowa', 'Człopa', 'Człuchów', 'Daleszyce', 'Darłowo', 'Debrzno', 'Dobczyce', 'Dobiegniew', 'Dobra', 'Dobre Miasto', 'Dobrodzień', 'Dobrzany', 'Dobrzyca', 'Dobrzyń nad Wisłą', 'Dolsk', 'Drawno', 'Drawsko Pomorskie', 'Drezdenko', 'Drobin', 'Drohiczyn', 'Drzewica', 'Dubiecko', 'Dukla', 'Duszniki-Zdrój', 'Dynów', 'Działdowo', 'Działoszyce', 'Działoszyn', 'Dzierzgoń', 'Dzierżoniów', 'Dziwnów', 'Dąbie', 'Dąbrowa Białostocka', 'Dąbrowa Górnicza', 'Dąbrowa Tarnowska', 'Dębica', 'Dęblin', 'Dębno', 'Elbląg', 'Ełk', 'Frampol', 'Frombork', 'Garwolin', 'Gdańsk', 'Gdynia', 'Giżycko', 'Glinojeck', 'Gliwice', 'Gniew', 'Gniewkowo', 'Gniezno', 'Gogolin', 'Golczewo', 'Goleniów', 'Golina', 'Golub-Dobrzyń', 'Goniądz', 'Goraj', 'Gorlice', 'Gorzów Wielkopolski', 'Gorzów Śląski', 'Gostynin', 'Gostyń', 'Gozdnica', 'Gołańcz', 'Gołdap', 'Gościno', 'Grabów nad Prosną', 'Grajewo', 'Grodków', 'Grodzisk Mazowiecki', 'Grodzisk Wielkopolski', 'Grudziądz', 'Grybów', 'Gryfice', 'Gryfino', 'Gryfów Śląski', 'Grójec', 'Guben', 'Gubin', 'Góra', 'Góra Kalwaria', 'Górowo Iławeckie', 'Górzno', 'Gąbin', 'Głogów', 'Głogów Małopolski', 'Głogówek', 'Głowno', 'Głubczyce', 'Głuchołazy', 'Głuszyca', 'Hajnówka', 'Halinów', 'Hel', 'Hrubieszów', 'Imielin', 'Inowrocław', 'Iwonicz-Zdrój', 'Izbica Kujawska', 'Iława', 'Iłowa', 'Iłża', 'Ińsko', 'Jabłonowo Pomorskie', 'Janikowo', 'Janowiec Wielkopolski', 'Janów Lubelski', 'Jaraczewo', 'Jarocin', 'Jarosław', 'Jasień', 'Jastarnia', 'Jastrowie', 'Jastrzębie-Zdrój', 'Jasło', 'Jawor', 'Jaworzno', 'Jaworzyna Śląska', 'Jedlicze', 'Jedlina-Zdrój', 'Jedwabne', 'Jelcz-Laskowice', 'Jelenia Góra', 'Jeziorany', 'Jordanów', 'Jutrosin', 'Józefów', 'Józefów nad Wisłą', 'Jędrzejów', 'Kalety', 'Kalisz', 'Kalisz Pomorski', 'Kalwaria Zebrzydowska', 'Kamieniec Ząbkowicki', 'Kamienna Góra', 'Kamień Krajeński', 'Kamień Pomorski', 'Kamieńsk', 'Kamionka', 'Karczew', 'Kargowa', 'Karlino', 'Karpacz', 'Kartuzy', 'Katowice', 'Kazimierz Dolny', 'Kazimierza Wielka', 'Kałuszyn', 'Kańczuga', 'Kcynia', 'Kielce', 'Kietrz', 'Kisielice', 'Kleczew', 'Kleszczele', 'Klimontów', 'Kluczbork', 'Knurów', 'Knyszyn', 'Kobylin', 'Kobyłka', 'Kolbuszowa', 'Kolno', 'Kolonowskie', 'Koluszki', 'Koniecpol', 'Konin', 'Konstancin-Jeziorna', 'Konstantynów Łódzki', 'Koprzywnica', 'Korfantów', 'Koronowo', 'Korsze', 'Kostrzyn', 'Kostrzyn nad Odrą', 'Koszalin', 'Koszyce', 'Kosów Lacki', 'Kowal', 'Kowalewo Pomorskie', 'Kowary', 'Koziegłowy', 'Kozienice', 'Kołaczyce', 'Koło', 'Kołobrzeg', 'Końskie', 'Kościan', 'Kościerzyna', 'Koźmin Wielkopolski', 'Koźminek', 'Kożuchów', 'Krajenka', 'Kraków', 'Krapkowice', 'Krasnobród', 'Krasnystaw', 'Kraśnik', 'Krobia', 'Krosno', 'Krosno Odrzańskie', 'Krotoszyn', 'Krośniewice', 'Kruszwica', 'Krynica Morska', 'Krynica-Zdrój', 'Krynki', 'Krzanowice', 'Krzepice', 'Krzeszowice', 'Krzywiń', 'Krzyż Wielkopolski', 'Książ Wielkopolski', 'Kudowa-Zdrój', 'Kunów', 'Kutno', 'Kuźnia Raciborska', 'Kwidzyn', 'Kórnik', 'Kąty Wrocławskie', 'Kędzierzyn-Koźle', 'Kępice', 'Kępno', 'Kętrzyn', 'Kęty', 'Kłecko', 'Kłobuck', 'Kłodawa', 'Kłodzko', 'Lebus', 'Legionowo', 'Legnica', 'Lesko', 'Leszno', 'Lewin Brzeski', 'Leśna', 'Leśnica', 'Leżajsk', 'Libiąż', 'Lidzbark', 'Lidzbark Warmiński', 'Limanowa', 'Lipiany', 'Lipno', 'Lipsk', 'Lipsko', 'Lubaczów', 'Lubartów', 'Lubawa', 'Lubawka', 'Lubań', 'Lubień Kujawski', 'Lubin', 'Lublin', 'Lubliniec', 'Lubniewice', 'Lubomierz', 'Lubowidz', 'Luboń', 'Lubraniec', 'Lubsko', 'Lubycza Królewska', 'Lututów', 'Lwówek', 'Lwówek Śląski', 'Lądek-Zdrój', 'Lębork', 'Lędziny', 'Maków Mazowiecki', 'Maków Podhalański', 'Malbork', 'Margonin', 'Marki', 'Maszewo', 'Małogoszcz', 'Małomice', 'Miasteczko Śląskie', 'Miastko', 'Michałowo', 'Miechów', 'Miejska Górka', 'Mielec', 'Mielno', 'Mieroszów', 'Mieszkowice', 'Mikołajki', 'Mikołów', 'Mikstat', 'Milanówek', 'Milicz', 'Mirosławiec', 'Mirsk', 'Międzybórz', 'Międzychód', 'Międzylesie', 'Międzyrzec Podlaski', 'Międzyrzecz', 'Międzyzdroje', 'Miłakowo', 'Miłomłyn', 'Miłosław', 'Mińsk Mazowiecki', 'Modliborzyce', 'Mogielnica', 'Mogilno', 'Morawica', 'Mordy', 'Moryń', 'Morąg', 'Mosina', 'Mońki', 'Mrocza', 'Mrozy', 'Mrągowo', 'Mszana Dolna', 'Mszczonów', 'Murowana Goślina', 'Muszyna', 'Myszków', 'Myszyniec', 'Mysłowice', 'Myślenice', 'Myślibórz', 'Mława', 'Młynary', 'Nakło nad Notecią', 'Namysłów', 'Narol', 'Nasielsk', 'Nałęczów', 'Nekla', 'Nidzica', 'Niemcza', 'Niemodlin', 'Niepołomice', 'Nieszawa', 'Nisko', 'Nowa Dęba', 'Nowa Ruda', 'Nowa Sarzyna', 'Nowa Sól', 'Nowa Słupia', 'Nowe', 'Nowe Brzesko', 'Nowe Miasteczko', 'Nowe Miasto Lubawskie', 'Nowe Miasto nad Pilicą', 'Nowe Skalmierzyce', 'Nowe Warpno', 'Nowogard', 'Nowogrodziec', 'Nowogród', 'Nowogród Bobrzański', 'Nowy Dwór Gdański', 'Nowy Dwór Mazowiecki', 'Nowy Korczyn', 'Nowy Staw', 'Nowy Sącz', 'Nowy Targ', 'Nowy Tomyśl', 'Nowy Wiśnicz', 'Nysa', 'Oborniki', 'Oborniki Śląskie', 'Obrzycko', 'Odolanów', 'Ogrodzieniec', 'Okonek', 'Olecko', 'Olesno', 'Oleszyce', 'Oleśnica', 'Olkusz', 'Olsztyn', 'Olsztynek', 'Olszyna', 'Opalenica', 'Opatowiec', 'Opatów', 'Opatówek', 'Opoczno', 'Opole', 'Opole Lubelskie', 'Orneta', 'Orzesze', 'Orzysz', 'Osieczna', 'Osiek', 'Ostritz', 'Ostroróg', 'Ostrowiec Świętokrzyski', 'Ostrołęka', 'Ostrzeszów', 'Ostróda', 'Ostrów Lubelski', 'Ostrów Mazowiecka', 'Ostrów Wielkopolski', 'Otmuchów', 'Otwock', 'Otyń', 'Ozimek', 'Ozorków', 'Oława', 'Ośno Lubuskie', 'Oświęcim', 'Ożarów', 'Ożarów Mazowiecki', 'Pabianice', 'Pacanów', 'Paczków', 'Pajęczno', 'Pakość', 'Parczew', 'Pasym', 'Pasłęk', 'Pelplin', 'Pełczyce', 'Piaseczno', 'Piaski', 'Piastów', 'Piechowice', 'Piekary Śląskie', 'Pieniężno', 'Pierzchnica', 'Pieszyce', 'Pieńsk', 'Pilawa', 'Pilica', 'Pilzno', 'Pionki', 'Piotrków Kujawski', 'Piotrków Trybunalski', 'Pisz', 'Piwniczna-Zdrój', 'Piątek', 'Piła', 'Piława Górna', 'Pińczów', 'Pleszew', 'Pniewy', 'Pobiedziska', 'Poddębice', 'Podkowa Leśna', 'Pogorzela', 'Polanica-Zdrój', 'Polanów', 'Police', 'Polkowice', 'Poniatowa', 'Poniec', 'Poręba', 'Poznań', 'Połaniec', 'Połczyn-Zdrój', 'Prabuty', 'Praszka', 'Prochowice', 'Proszowice', 'Pruchnik', 'Prudnik', 'Prusice', 'Pruszcz Gdański', 'Pruszków', 'Przasnysz', 'Przecław', 'Przedbórz', 'Przedecz', 'Przemków', 'Przemyśl', 'Przeworsk', 'Przysucha', 'Prószków', 'Pszczyna', 'Pszów', 'Puck', 'Puszczykowo', 'Puławy', 'Pułtusk', 'Pyrzyce', 'Pyskowice', 'Pyzdry', 'Płock', 'Płoty', 'Płońsk', 'Rabka-Zdrój', 'Racibórz', 'Raciąż', 'Radków', 'Radlin', 'Radom', 'Radomsko', 'Radomyśl Wielki', 'Radoszyce', 'Radymno', 'Radziejów', 'Radzionków', 'Radzymin', 'Radzyń Chełmiński', 'Radzyń Podlaski', 'Radłów', 'Rajgród', 'Rakoniewice', 'Raszków', 'Rawa Mazowiecka', 'Rawicz', 'Recz', 'Reda', 'Rejowiec', 'Rejowiec Fabryczny', 'Resko', 'Reszel', 'Rogoźno', 'Ropczyce', 'Ruciane-Nida', 'Ruda Śląska', 'Rudnik nad Sanem', 'Rumia', 'Rybnik', 'Rychwał', 'Rydułtowy', 'Rydzyna', 'Ryglice', 'Ryki', 'Rymanów', 'Ryn', 'Rypin', 'Rzepin', 'Rzeszów', 'Rzgów', 'Różan', 'Sandomierz', 'Sanniki', 'Sanok', 'Sejny', 'Serock', 'Sianów', 'Siechnice', 'Siedlce', 'Siedliszcze', 'Siemianowice Śląskie', 'Siemiatycze', 'Sieniawa', 'Sieradz', 'Sieraków', 'Sierpc', 'Siewierz', 'Skalbmierz', 'Skarszewy', 'Skaryszew', 'Skarżysko-Kamienna', 'Skawina', 'Skała', 'Skierniewice', 'Skoczów', 'Skoki', 'Skwierzyna', 'Skórcz', 'Skępe', 'Sobótka', 'Sochaczew', 'Sochocin', 'Sokołów Małopolski', 'Sokołów Podlaski', 'Sokółka', 'Solec Kujawski', 'Solec nad Wisłą', 'Sompolno', 'Sopot', 'Sosnowiec', 'Sośnicowice', 'Stalowa Wola', 'Starachowice', 'Stargard', 'Starogard Gdański', 'Stary Sącz', 'Staszów', 'Stawiski', 'Stawiszyn', 'Stepnica', 'Stoczek Łukowski', 'Stopnica', 'Stronie Śląskie', 'Strumień', 'Stryków', 'Strzegom', 'Strzelce Krajeńskie', 'Strzelce Opolskie', 'Strzelin', 'Strzelno', 'Strzyżów', 'Stąporków', 'Stęszew', 'Sucha Beskidzka', 'Suchań', 'Suchedniów', 'Suchowola', 'Sulechów', 'Sulejów', 'Sulejówek', 'Sulmierzyce', 'Sulęcin', 'Supraśl', 'Suraż', 'Susz', 'Suwałki', 'Sułkowice', 'Swarzędz', 'Syców', 'Szadek', 'Szamocin', 'Szamotuły', 'Szczawnica', 'Szczawno-Zdrój', 'Szczebrzeszyn', 'Szczecin', 'Szczecinek', 'Szczekociny', 'Szczucin', 'Szczuczyn', 'Szczyrk', 'Szczytna', 'Szczytno', 'Szepietowo', 'Szklarska Poręba', 'Szlichtyngowa', 'Szprotawa', 'Sztum', 'Szubin', 'Szydłowiec', 'Szydłów', 'Sędziszów', 'Sędziszów Małopolski', 'Sępopol', 'Sępólno Krajeńskie', 'Sława', 'Sławków', 'Sławno', 'Słomniki', 'Słubice', 'Słupca', 'Słupsk', 'Tarczyn', 'Tarnobrzeg', 'Tarnogród', 'Tarnowskie Góry', 'Tarnów', 'Tczew', 'Terespol', 'Tolkmicko', 'Tomaszów Lubelski', 'Tomaszów Mazowiecki', 'Toruń', 'Torzym', 'Toszek', 'Trzcianka', 'Trzciel', 'Trzcińsko-Zdrój', 'Trzebiatów', 'Trzebinia', 'Trzebnica', 'Trzemeszno', 'Tuchola', 'Tuchów', 'Tuczno', 'Tuliszków', 'Turek', 'Tuszyn', 'Tułowice', 'Twardogóra', 'Tychowo', 'Tychy', 'Tyczyn', 'Tykocin', 'Tyszowce', 'Tłuszcz', 'Ujazd', 'Ujście', 'Ulanów', 'Uniejów', 'Urzędów', 'Ustka', 'Ustroń', 'Ustrzyki Dolne', 'Wadowice', 'Warka', 'Warszawa', 'Warta', 'Wasilków', 'Wałbrzych', 'Wałcz', 'Wejherowo', 'Wielbark', 'Wieleń', 'Wielichowo', 'Wieliczka', 'Wieluń', 'Wieruszów', 'Wilamowice', 'Wiskitki', 'Wisła', 'Witkowo', 'Witnica', 'Wiązów', 'Więcbork', 'Wiślica', 'Wleń', 'Wodzisław', 'Wodzisław Śląski', 'Wojcieszów', 'Wojkowice', 'Wojnicz', 'Wolbrom', 'Wolbórz', 'Wolin', 'Wolsztyn', 'Wołczyn', 'Wołomin', 'Wołów', 'Woźniki', 'Wrocław', 'Wronki', 'Września', 'Wschowa', 'Wyrzysk', 'Wysoka', 'Wysokie Mazowieckie', 'Wyszków', 'Wyszogród', 'Wyśmierzyce', 'Wąbrzeźno', 'Wąchock', 'Wągrowiec', 'Wąsosz', 'Węgliniec', 'Węgorzewo', 'Węgorzyno', 'Węgrów', 'Władysławowo', 'Włocławek', 'Włodawa', 'Włoszczowa', 'Zabrze', 'Zabłudów', 'Zagórz', 'Zagórów', 'Zakliczyn', 'Zaklików', 'Zakopane', 'Zakroczym', 'Zalewo', 'Zambrów', 'Zamość', 'Zator', 'Zawadzkie', 'Zawichost', 'Zawidów', 'Zawiercie', 'Zbąszynek', 'Zbąszyń', 'Zduny', 'Zduńska Wola', 'Zdzieszowice', 'Zelów', 'Zgierz', 'Zgorzelec', 'Zielona Góra', 'Zielonka', 'Ziębice', 'Zwierzyniec', 'Zwoleń', 'Ząbki', 'Ząbkowice Śląskie', 'Złocieniec', 'Złoczew', 'Złotoryja', 'Złoty Stok', 'Złotów', 'Ćmielów', 'Łabiszyn', 'Łagów', 'Łapy', 'Łasin', 'Łask', 'Łaskarzew', 'Łaszczów', 'Łaziska Górne', 'Łazy', 'Łańcut', 'Łeba', 'Łobez', 'Łobżenica', 'Łochów', 'Łomianki', 'Łomża', 'Łosice', 'Łowicz', 'Łuków', 'Łódź', 'Łęczna', 'Łęczyca', 'Łęknica', 'Ścinawa', 'Ślesin', 'Śmigiel', 'Śrem', 'Środa Wielkopolska', 'Środa Śląska', 'Świdnica', 'Świdnik', 'Świdwin', 'Świebodzice', 'Świebodzin', 'Świecie', 'Świeradów-Zdrój', 'Świerzawa', 'Świnoujście', 'Świątniki Górne', 'Świętochłowice', 'Żabno', 'Żagań', 'Żarki', 'Żary', 'Żarów', 'Żelechów', 'Żerków', 'Żmigród', 'Żnin', 'Żory', 'Żukowo', 'Żuromin', 'Żychlin', 'Żyrardów', 'Żywiec'
] 

def create_cities(apps, schema_editor):
    City = apps.get_model('users', 'City')
    for city in CITIES:
        City.objects.create(name=city)

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chats', '0001_initial'),
        ('products', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=100, verbose_name='first name')),
                ('last_name', models.CharField(max_length=100, verbose_name='last name')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='phone')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('X', 'Other')], default='X', max_length=1, verbose_name='gender')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_activated', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(default='../static/images/blank.jpg', help_text='Upload an avatar', upload_to='images/profile_pics', verbose_name='image')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Cities',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(blank=True, max_length=55, null=True, unique=True)),
                ('visited_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReportUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(blank=True, max_length=200, null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('report_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports_author', to=settings.AUTH_USER_MODEL)),
                ('reported_message', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report', to='chats.message')),
                ('user_reported', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports_subject', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Report',
                'verbose_name_plural': 'User Reports',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=250)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('upvoted_by', models.ManyToManyField(blank=True, related_name='upvoted_posts', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='useraccount',
            name='location',
            field=models.ForeignKey(max_length=35, on_delete=django.db.models.deletion.CASCADE, to='users.city', verbose_name='location(city)'),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='wishlist',
            field=models.ManyToManyField(blank=True, related_name='wishlists', to='products.Product'),
        ),
        migrations.CreateModel(
            name='Blacklist',
            fields=[
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='blacklist', serialize=False, to='users.useraccount')),
                ('blocked_users', models.ManyToManyField(blank=True, related_name='blocked_by_others', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(create_cities),
    ]
