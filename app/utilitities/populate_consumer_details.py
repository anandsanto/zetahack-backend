#!/usr/bin/env python3

import aiohttp
import asyncio
import json
import random as rd
import datetime as dt

random_names = ["Bogdan Curran", "Brandon Mccray", "Anish Wynn", "Alexandros Hancock", "Nabiha Johnson", "Gaia Sutherland", "Joan Stark", "Edwin Clay", "Harriett Higgins", "Marco Talbot", "Ellie-Rose Browne", "Iwan Hayden", "Nellie Huang", "Madison Stamp", "Lacey-Mae Tillman", "Arnas Markham", "Yazmin Woodcock", "Maria Jaramillo", "Mariyah Head", "Eesa Deacon", "Abdullahi Barnard", "Angela Jackson", "Stephan Hamilton", "Kayan Good", "Lillie Mayo", "Hollie Pace", "Sameer Li", "Taya Holloway", "Ellesse Gamble", "Huzaifa Denton", "Melina Velazquez", "Anastasia Bowes", "Jean Schofield", "Beulah Mcgowan", "Ava Finnegan", "Reanna Melton", "Garfield Mooney", "Ezekiel Hess", "Issa Muir", "Rodney Watt", "Margot Gibbs", "Fateh Curry", "Phillipa Lindsay", "Alfie-Jay Noble", "Neive Stokes", "Evie-Rose Cassidy", "Stephen Mcneil", "Sumaiya Bradley", "Fionn Krause", "Jayson Bush", "Kelsi Shaw", "Elaina Byers", "Sienna-Rose Andersen", "Silas Timms", "Karla Monaghan", "Kean Thorne", "Kirstin Currie", "Tahmid Carty", "Samad Higgs", "Rafe Davey", "Amy Mcfarland", "Cairo Hebert", "Macey Gale", "Finn Mcgregor", "Osman Eastwood", "Nahla Clegg", "Tevin Fox", "Cleo Humphrey", "Jayne Parker", "Milena Glover", "Izzie Aldred", "Aiysha Walmsley", "Ana Kaiser", "Kristin Hansen", "Astrid Richards", "Kellie Gilbert", "Stefanie Acevedo", "Arfa Hayes", "Faiz Vincent", "Lily-Mai Britt", "Kaison Hunt", "Ayyan Perez", "Rihanna Little", "Harvie Moon", "Duncan Wallace", "Casper Dupont", "Elena Stacey", "Kason Metcalfe", "Alysha Sanchez", "Farhana Cullen", "Faizah Armitage", "Cindy Dalton", "Vishal Monroe", "Zunairah Bone", "Barbara Pittman", "Mylie Olson", "Kaydee Blankenship", "Ceri Read", "Akram O'Ryan"]
phone_prefix = ['+91', '']
#url = "https://zetahack-backend.herokuapp.com/general/api/addseller"
url = "http://127.0.0.1:8000/general/api/addcust"

async def add_seller(session, idnum):
    dat = {}
    name = rd.choice(random_names)
    dat["age"] = rd.randint(18, 100)
    dat["customer_id"] = str(idnum)
    dat["first_name"] = name.split()[0]
    dat["last_name"] = name.split()[1]
    dat['phone'] = rd.choice(phone_prefix) + ''.join([str(rd.randint(1, 9)) for i in range(10)])
    dat['address'] = "No 4, Viveganandhar Theru, Dubai Kurukku Sandhu, Dubai Main Rd, Dubai"
    dat['member_since'] = str(dt.datetime.now() - dt.timedelta(days=rd.randint(100, 1000)))

    print(dat)
    async with session.post(url, json=dat) as resp:
        data = await resp.json(content_type='application/json')
        stat = resp.status
        print(data, stat)

async def gather():
    fns = []
    async with aiohttp.ClientSession() as session:
        for i in range(1, 50):
            print("Done")
            fns.append(await add_seller(session, i))
        await asyncio.gather(*fns)

asyncio.run(gather())
