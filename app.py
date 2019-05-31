import os
import re
import sqlite3
from flask import Flask, redirect, url_for, request, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from tika import parser
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.secret_key = 'admin_password'
path = app.instance_path+"\data_obat.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+path
conn = sqlite3.connect(path)
cur = conn.cursor()
db = SQLAlchemy(app)

class DataObat(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	NAMA_OBAT = db.Column(db.Text)
	NAMA_GENERIK = db.Column(db.Text)
	NAMA_KELAS = db.Column(db.Text)
	KANDUNGAN = db.Column(db.Text)
	INDIKASI = db.Column(db.Text)
	KONTRA_INDIKASI = db.Column(db.Text)
	EFEK_SAMPING = db.Column(db.Text)
	INTERAKSI_OBAT = db.Column(db.Text)

	def __init__(self, id, NAMA_OBAT, NAMA_GENERIK, NAMA_KELAS, KANDUNGAN, INDIKASI, KONTRA_INDIKASI, EFEK_SAMPING, INTERAKSI_OBAT):
		self.id = id
		self.NAMA_OBAT = NAMA_OBAT
		self.NAMA_GENERIK = NAMA_GENERIK
		self.NAMA_KELAS = NAMA_KELAS
		self.KANDUNGAN = KANDUNGAN
		self.INDIKASI = INDIKASI
		self.KONTRA_INDIKASI = KONTRA_INDIKASI
		self.EFEK_SAMPING = EFEK_SAMPING
		self.INTERAKSI_OBAT = INTERAKSI_OBAT


@app.route("/")
def init():
	return redirect(url_for('login'))

@app.route("/login", methods=['POST','GET'])
def login():
	if request.method == 'POST':
		password = request.form['passwordadmin']
		if password == 'admin123':
			return redirect(url_for('home'))
		else:
			flash('Password salah!')
	return render_template('login.html')

@app.route("/home", methods=['POST','GET'])
def home():
	conn = sqlite3.connect(path)
	cursor = conn.cursor()

	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			cursor.execute("")
			filename = secure_filename(file.filename)
			print('File saving...')
			file.save(os.path.join(app.instance_path, filename))
			print('File saved!')
			flash('File uploaded!')
			parse_file(filename)
			print('File parsed!')
			flash('File parsed!')
			print('Data added!')
		else:
			print('File not allowed!')

	cursor.execute("SELECT * FROM data_obat")

	return render_template('home.html', all_data = cursor.fetchall())

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_file(filename):
	conn = sqlite3.connect(path)
	cursor = conn.cursor()

	file = os.path.join(app.instance_path, filename)
	parsedfile = open("static\\parsed.txt","w",  encoding='utf8')
	# Parse data from file
	file_data = parser.from_file(file)
	print("File Parsed!")
	# Get files text content
	text = file_data['content']
	parsedfile.write(text)
	print("Output File Created!")
	parsedfile.close()
	# Remove first 25 lines
	with open('static\\parsed.txt', 'r') as fin:
		data = fin.read().splitlines(True)
	with open('static\\parsed.txt', 'w') as fout:
		fout.writelines(data[23:])

	read_file = open('static\\parsed.txt', 'r')
	cursor.execute("SELECT COUNT(*) FROM data_obat")
	total_row = cursor.fetchone()[0]
	print(total_row)

	doi_title_pattern = "( : \n)"
	list_data = []
	isComplete = False
	for line in read_file:
		if re.search(doi_title_pattern,line) or not re.search(". \n",line):
			print("Skipped")
		else:
			print(line)
			list_data.append(line)

		if len(list_data) == 8:
			total_row = total_row+1;
			add_data(total_row+1,list_data[0], list_data[1], list_data[2], list_data[3], list_data[4], list_data[5], list_data[6], list_data[7])
			print("Data added!")


	print("OLRAIT")
	for listed in list_data:
		print(listed)

def add_data(id,namaobat, namagenerik, namakelas, kandungan, indikasi, kontraindikasi, efeksamping, interaksiobat):
	new_data = DataObat(id,namaobat,namagenerik,namakelas,kandungan,indikasi,kontraindikasi,efeksamping,interaksiobat)
	db.session.add(new_data)
	db.session.commit()

def update_table():
	conn = sqlite3.connect(path)
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM data_obat")
	all_data = cursor.fetchall()


if __name__ == "__main__":
	app.run()