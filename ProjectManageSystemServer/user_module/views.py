from django.shortcuts import render

# Create your views here.

def register(data):
	un = data['username']
	pw = data['password']
	em = data['email']
	code = data['code']

def login(data):
	un = data['username']
	pw = data['password']

