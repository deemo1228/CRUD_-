from flask_seeder import Seeder
from index import City      #因為要加入的資料表為City所以要把它從idnex引進來


class DemoSeeder(Seeder):
    def run(self):
        insert_row = [              #要加入的資料
            {
                'city_name': 'Taipei'
            },
            {
                'city_name': 'New Taipei'
            },
            {
                'city_name': 'Taoyuan'
            },
            {
                'city_name': 'Taichung'
            },
            {
                'city_name': 'Tainan'
            },
            {
                'city_name': 'Kaohsiung'
            }
        ]
        for row in insert_row:
            print(row['city_name'])     #印出你加入了哪一些東西
            insert_city = City(name=row['city_name'])       #在City這張表下加入row這個陣列當中naem=row['city_name']
            self.db.session.add(insert_city)                #把inser_city存入暫存，seed會自動幫你commit
