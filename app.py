import os
from flask import Flask, redirect, url_for, request, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from tika import parser
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.secret_key = 'admin_password'
path = app.instance_path+"\data_obat.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+path
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
	
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			print('File saving...')
			file.save(os.path.join(app.instance_path, filename))
			print('File saved!')
			flash('File uploaded!')
			parse_file(filename)
			print('File parsed!')
			flash('File parsed!')
			add_data(2,'data','ini','hanya','untuk','coba','coba','terima','kasih')
			print('Data added!')
		else:
			print('File not allowed!')

	return render_template('home.html')

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_file(filename):
	file = os.path.join(app.instance_path, filename)
	parsedfile = open("static\\parsed.txt","w")
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
		fout.writelines(data[25:])

def add_data(id, namaobat, namagenerik, namakelas, kandungan, indikasi, kontraindikasi, efeksamping, interaksiobat):
	new_data = DataObat(id,namaobat,namagenerik,namakelas,kandungan,indikasi,kontraindikasi,efeksamping,interaksiobat)
	db.session.add(new_data)
	db.session.commit()

if __name__ == "__main__":
	app.run()