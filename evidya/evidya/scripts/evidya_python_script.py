"""Tripadvisorreviews webcheckin run file"""
import os
import csv
import json
import md5
import traceback
import MySQLdb

class Tripadvisor(object):
    """ Starting class """
    def __init__(self):
        self.conn = MySQLdb.connect(db='EVIDYA',user='root',passwd='hdrn59!',
                                charset="utf8",host='localhost',use_unicode=True)
        self.cur = self.conn.cursor()
        self.conn.set_character_set('utf8')
        self.cur.execute('SET NAMES utf8;')
        self.cur.execute('SET CHARACTER SET utf8;')
        self.cur.execute('SET character_set_connection=utf8;')
        self.insert_query = "INSERT INTO evidya_crawl(sk, state_name, district_name, crawl_status, aux_info, created_at, modified_at, last_seen) values(%s,%s,%s,%s,%s,now(),now(),now()) on duplicate key update modified_at = now()"

    def main(self):
        with open('information.json') as json_data:
            data = json.load(json_data)
            for keym, valuem in data.iteritems():
                if keym in ['09', '23', '27', '29']:
                    state_name = valuem[-1]
                    district_name = valuem[0].values()
                    for dis in district_name:
                        sk = md5.md5(state_name+dis).hexdigest()
                        values = (sk, state_name, dis, 0, '')
                        self.cur.execute(self.insert_query , values)
        print 'here'

if __name__ == "__main__":
        Tripadvisor().main()

"""
table schema CREATE TABLE `evidya_crawl` (
  `sk` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `state_name` text CHARACTER SET utf8,
  `district_name` text CHARACTER SET utf8,
  `crawl_status` int(3) NOT NULL DEFAULT '0',
  `aux_info` text CHARACTER SET utf8,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen` datetime NOT NULL,
  PRIMARY KEY (`sk`),
  KEY `sk` (`sk`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci
"""

