from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import re


asd = ['AndresAA', 'Pancakes', 'Pancakes', 'X-Pelox', 'Pancakes', 'Jerich', 'Pancakes', 'X-Pelox', 'AndresAA', 'X-Pelox', 'Pancakes', 'Jerich', 'Pancakes', 'Angelini', 'Tobio', 'Jerich', 'Pancakes', 'Spade', 'Zeliox SwordCloud', 'AndresAA', 'Tobio', 'Zeliox SwordCloud', 'Spade', 'Pancakes', 'LuichoX', 'X-Pelox', 'Hidan', 'Jerich', 'Hiro', 'Toxucroc', 'Cismu', 'Zeliox SwordCloud', "Ale Hershey's", 'Tobio', 'Hidan', 'Tobio', 'Jean Papitas', 'Cismu', 'LuichoX', "Ale Hershey's", 'Hiro', 'Angelini', 'DIO', 'Angelini', 'Toxucroc', 'AndresAA', 'Cismu', 'Konami', 
'Diowo', 'Spade', 'Blate', 'Hiro', 'Flye', 'Jean Papitas', 'Hidan', 'LuichoX', 'Rookie355', 'Pancakes', 'DIO', 'Anriot', 'Farre', 'X-Pelox', 'Lum1', 'Blate', 'Flye', 'apselito', 'Difox', 'LIMIT', 'Agui', 'Diowo', 'Valgarite', 'Danilopaz1', 'Tino22', 'Hidan', 'Cax', 'Farre', 'DIO', 'Rookie355', 'Lum1', 'Difox', 'apselito', 'Tino22', 'Danilopaz1']

print(len(asd))