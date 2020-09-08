#!/usr/bin/env python
# example: run on 2019-12-31 with
#./partition_manage.py -v -H srv-log-srf-02 -A fcslog-replica-01 -d hdbpp -a hdbpparchive -u root -y 2020
#./partition_manage.py -v --host srv-log-srf-02 --hostarchive fcslog-replica-01 --database hdbpp --databasearchive hdbpparchive -u root -y 2020

import sys
import mysql.connector
from mysql.connector import errorcode
import getpass
from optparse import OptionParser

tableNames=["att_history","att_parameter",
"att_scalar_devboolean_ro","att_scalar_devboolean_rw","att_array_devboolean_ro","att_array_devboolean_rw",
"att_scalar_devuchar_ro","att_scalar_devuchar_rw","att_array_devuchar_ro","att_array_devuchar_rw",
"att_scalar_devshort_ro","att_scalar_devshort_rw","att_array_devshort_ro","att_array_devshort_rw",
"att_scalar_devushort_ro","att_scalar_devushort_rw","att_array_devushort_ro","att_array_devushort_rw",
"att_scalar_devlong_ro","att_scalar_devlong_rw","att_array_devlong_ro","att_array_devlong_rw",
"att_scalar_devulong_ro","att_scalar_devulong_rw","att_array_devulong_ro","att_array_devulong_rw",
"att_scalar_devlong64_ro","att_scalar_devlong64_rw","att_array_devlong64_ro","att_array_devlong64_rw",
"att_scalar_devulong64_ro","att_scalar_devulong64_rw","att_array_devulong64_ro","att_array_devulong64_rw",
"att_scalar_devfloat_ro","att_scalar_devfloat_rw","att_array_devfloat_ro","att_array_devfloat_rw",
"att_scalar_devdouble_rw","att_array_devdouble_ro","att_array_devdouble_rw",
"att_scalar_devstring_ro","att_scalar_devstring_rw","att_array_devstring_ro","att_array_devstring_rw",
"att_scalar_devstate_ro","att_scalar_devstate_rw","att_array_devstate_ro","att_array_devstate_rw",
"att_scalar_devencoded_ro","att_scalar_devencoded_rw","att_array_devencoded_ro","att_array_devencoded_rw",
"att_scalar_devenum_ro","att_scalar_devenum_rw","att_array_devenum_ro","att_array_devenum_rw"]

dbpassword=""

reorganizeFutureQuery=("ALTER TABLE %s.%s REORGANIZE PARTITION future INTO"
"("
"  PARTITION p%d VALUES LESS THAN ('%d-01-01'),"
"  PARTITION future       VALUES LESS THAN MAXVALUE"
");\n"
"ALTER TABLE %s.%s ANALYZE PARTITION p%d;")

reorganizeFutureQueryDoubleRo=("ALTER TABLE %s.att_scalar_devdouble_ro REORGANIZE PARTITION future INTO"
"("
"  PARTITION p%d_01_02 VALUES LESS THAN ('%d-03-01'),"
"  PARTITION p%d_03_04 VALUES LESS THAN ('%d-05-01'),"
"  PARTITION p%d_05_06 VALUES LESS THAN ('%d-07-01'),"
"  PARTITION p%d_07_08 VALUES LESS THAN ('%d-09-01'),"
"  PARTITION p%d_09_10 VALUES LESS THAN ('%d-11-01'),"
"  PARTITION p%d_11_12 VALUES LESS THAN ('%d-01-01'),"
"  PARTITION future       VALUES LESS THAN MAXVALUE"
");\n"
"ALTER TABLE %s.att_scalar_devdouble_ro ANALYZE PARTITION p%d_01_02;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro ANALYZE PARTITION p%d_03_04;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro ANALYZE PARTITION p%d_05_06;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro ANALYZE PARTITION p%d_07_08;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro ANALYZE PARTITION p%d_09_10;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro ANALYZE PARTITION p%d_11_12;\n")

exchangePastQuery=(""
"ALTER TABLE %s.%s EXCHANGE PARTITION p%d WITH TABLE %s.%s_tmp WITHOUT VALIDATION;\n"
"ALTER TABLE %s.%s EXCHANGE PARTITION p%d WITH TABLE %s.%s_tmp WITHOUT VALIDATION;")

exchangePastQueryDoubleRo=(""
"ALTER TABLE %s.att_scalar_devdouble_ro EXCHANGE PARTITION p%d_01_02 WITH TABLE %s.att_scalar_devdouble_ro_tmp WITHOUT VALIDATION;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro EXCHANGE PARTITION p%d_01_02 WITH TABLE %s.att_scalar_devdouble_ro_tmp WITHOUT VALIDATION;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro EXCHANGE PARTITION p%d_03_04 WITH TABLE %s.att_scalar_devdouble_ro_tmp WITHOUT VALIDATION;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro EXCHANGE PARTITION p%d_03_04 WITH TABLE %s.att_scalar_devdouble_ro_tmp WITHOUT VALIDATION;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro EXCHANGE PARTITION p%d_05_06 WITH TABLE %s.att_scalar_devdouble_ro_tmp WITHOUT VALIDATION;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro EXCHANGE PARTITION p%d_05_06 WITH TABLE %s.att_scalar_devdouble_ro_tmp WITHOUT VALIDATION;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro EXCHANGE PARTITION p%d_07_08 WITH TABLE %s.att_scalar_devdouble_ro_tmp WITHOUT VALIDATION;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro EXCHANGE PARTITION p%d_07_08 WITH TABLE %s.att_scalar_devdouble_ro_tmp WITHOUT VALIDATION;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro EXCHANGE PARTITION p%d_09_10 WITH TABLE %s.att_scalar_devdouble_ro_tmp WITHOUT VALIDATION;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro EXCHANGE PARTITION p%d_09_10 WITH TABLE %s.att_scalar_devdouble_ro_tmp WITHOUT VALIDATION;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro EXCHANGE PARTITION p%d_11_12 WITH TABLE %s.att_scalar_devdouble_ro_tmp WITHOUT VALIDATION;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro EXCHANGE PARTITION p%d_11_12 WITH TABLE %s.att_scalar_devdouble_ro_tmp WITHOUT VALIDATION;")

reorganizePastQuery=(""
"ALTER TABLE %s.%s TRUNCATE PARTITION p%d;\n"
"ALTER TABLE %s.%s REORGANIZE PARTITION p000,p%d INTO "
"("
"  PARTITION p000 VALUES LESS THAN ('%d-01-01')"
");\n"
"ALTER TABLE %s.%s ANALYZE PARTITION p%d;\n"
"ALTER TABLE %s.%s ANALYZE PARTITION p000;")

reorganizePastQueryDoubleRo=(""
"ALTER TABLE %s.att_scalar_devdouble_ro TRUNCATE PARTITION p%d_01_02;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro TRUNCATE PARTITION p%d_03_04;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro TRUNCATE PARTITION p%d_05_06;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro TRUNCATE PARTITION p%d_07_08;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro TRUNCATE PARTITION p%d_09_10;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro TRUNCATE PARTITION p%d_11_12;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro REORGANIZE PARTITION p000,p%d_01_02,p%d_03_04,p%d_05_06,p%d_07_08,p%d_09_10,p%d_11_12 INTO "
"("
"  PARTITION p000 VALUES LESS THAN ('%d-01-01')"
");\n"
"ALTER TABLE %s.att_scalar_devdouble_ro ANALYZE PARTITION p%d_01_02;\n"
"ALTER TABLE %s.att_scalar_devdouble_ro ANALYZE PARTITION p000;")

updateAttConfErrorDescQuery=(""
"INSERT IGNORE INTO %s.att_conf (att_conf_id,att_name,att_conf_data_type_id,att_ttl,facility,domain,family,member,name) "
"SELECT att_conf_id,att_name,att_conf_data_type_id,att_ttl,facility,domain,family,member,name FROM %s.att_conf;\n"
"INSERT IGNORE INTO %s.att_error_desc (att_error_desc_id,error_desc) "
"SELECT att_error_desc_id,error_desc FROM %s.att_error_desc;"
)

testQuery=(""
"SELECT att_conf_id,att_name FROM %s.att_conf ORDER BY att_conf_id DESC LIMIT 3;"
)


def reorganize_future(dbhost, dbname, dbuser, dbpass, year):
	hdbpp=mysql.connector.MySQLConnection()
	try:
		if not options.verbose :
			hdbpp = mysql.connector.connect(host=dbhost,
				database=dbname,
				user=dbuser,
				password=dbpass)
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print ("HDB++: wrong username or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print ("HDB++: database not existing")
		else:
			print ("HDB++: " + err)
		hdbpp.close()
		return

	try:
		print ("-----------------------------------------\nReorganize future partitions on " + dbhost + "." + dbname + "\n-----------------------------------------\n")
		if not options.verbose :
			hdbppcursor = hdbpp.cursor(named_tuple=True, buffered=True)
		for table in tableNames:
			sql=reorganizeFutureQuery % (dbname,table,year,year+1,dbname,table,year)
			print sql
			if not options.verbose :
				# executing cursor with execute method and pass SQL query
				for result in hdbppcursor.execute(sql, multi=True):
					if result.with_rows:
						print("Rows produced by statement '{}':".format(result.statement))
						print(result.fetchall())
					else:
						print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
				hdbpp.commit()
		sql=reorganizeFutureQueryDoubleRo % (dbname,year,year,year,year,year,year,year,year,year,year,year,year+1,dbname,year,dbname,year,dbname,year,dbname,year,dbname,year,dbname,year)
		print sql
		if not options.verbose :
			# executing cursor with execute method and pass SQL query
			for result in hdbppcursor.execute(sql, multi=True):
				if result.with_rows:
					print("Rows produced by statement '{}':".format(result.statement))
					print(result.fetchall())
				else:
					print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
			hdbpp.commit()
			hdbppcursor.close()

		print("---------> Success\n\n")
	except Exception as e:
		print("---------> Warn: ", str(e))
		print("\n\n-------------------------------------------------\n\n")
		return


	hdbpp.close()


def exchange_past(dbhost, dbnamefrom, dbnameto, dbuser, dbpass, year):
	hdbpp=mysql.connector.MySQLConnection()
	try:
		if not options.verbose :
			hdbpp = mysql.connector.connect(host=dbhost,
				database=dbnameto,
				user=dbuser,
				password=dbpass)
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print ("HDB++: wrong username or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print ("HDB++: database not existing")
		else:
			print ("HDB++: " + err)
		hdbpp.close()
		return

	try:
		print ("-----------------------------------------\nExchange past partitions on " + dbhost + "." + dbnamefrom + " -> " + dbhost + "." + dbnameto + "\n-----------------------------------------\n")
		if not options.verbose :
			hdbppcursor = hdbpp.cursor(named_tuple=True, buffered=True)
		for table in tableNames:
			sql=exchangePastQuery % (dbnamefrom,table,year,dbnameto,table,dbnameto,table,year,dbnameto,table)
			print sql
			if not options.verbose :
				# executing cursor with execute method and pass SQL query
				for result in hdbppcursor.execute(sql, multi=True):
					if result.with_rows:
						print("Rows produced by statement '{}':".format(result.statement))
						print(result.fetchall())
					else:
						print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
				hdbpp.commit()
		sql=exchangePastQueryDoubleRo % (dbnamefrom,year,dbnameto,dbnameto,year,dbnameto, dbnamefrom,year,dbnameto,dbnameto,year,dbnameto, dbnamefrom,year,dbnameto,dbnameto,year,dbnameto, dbnamefrom,year,dbnameto,dbnameto,year,dbnameto, dbnamefrom,year,dbnameto,dbnameto,year,dbnameto, dbnamefrom,year,dbnameto,dbnameto,year,dbnameto)
		print sql
		if not options.verbose :
			# executing cursor with execute method and pass SQL query
			for result in hdbppcursor.execute(sql, multi=True):
				if result.with_rows:
					print("Rows produced by statement '{}':".format(result.statement))
					print(result.fetchall())
				else:
					print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
			hdbpp.commit()
			hdbppcursor.close()
		print("---------> Success\n\n")
	except Exception as e:
		print("---------> Warn: ", str(e))
		print("\n\n-------------------------------------------------\n\n")
		return

	hdbpp.close()


def reorganize_past(dbhost, dbname, dbuser, dbpass, year):
	hdbpp=mysql.connector.MySQLConnection()
	try:
		if not options.verbose :
			hdbpp = mysql.connector.connect(host=dbhost,
				database=dbname,
				user=dbuser,
				password=dbpass)
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print ("HDB++: wrong username or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print ("HDB++: database not existing")
		else:
			print ("HDB++: " + err)
		hdbpp.close()
		return

	try:
		print ("-----------------------------------------\nReorganize past partitions on " + dbhost + "." + dbname + "\n-----------------------------------------\n")
		if not options.verbose :
			hdbppcursor = hdbpp.cursor(named_tuple=True, buffered=True)
		for table in tableNames:
			sql=reorganizePastQuery % (dbname,table,year,dbname,table,year,year+1,dbname,table,year+1,dbname,table)
			print sql
			if not options.verbose :
				# executing cursor with execute method and pass SQL query
				for result in hdbppcursor.execute(sql, multi=True):
					if result.with_rows:
						print("Rows produced by statement '{}':".format(result.statement))
						print(result.fetchall())
					else:
						print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
				hdbpp.commit()
		sql=reorganizePastQueryDoubleRo % (dbname,year,dbname,year,dbname,year,dbname,year,dbname,year,dbname,year,dbname,year,year,year,year,year,year,year+1,dbname,year+1,dbname)
		print sql
		if not options.verbose :
			# executing cursor with execute method and pass SQL query
			for result in hdbppcursor.execute(sql, multi=True):
				if result.with_rows:
					print("Rows produced by statement '{}':".format(result.statement))
					print(result.fetchall())
				else:
					print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
			hdbpp.commit()
			hdbppcursor.close()
		print("---------> Success\n\n")
	except Exception as e:
		print("---------> Warn: ", str(e))
		print("\n\n-------------------------------------------------\n\n")
		return

	hdbpp.close()

def update_att_conf_error_desc(dbhost, dbnamefrom, dbnameto, dbuser, dbpass):
	hdbpp=mysql.connector.MySQLConnection()
	try:
		if not options.verbose :
			hdbpp = mysql.connector.connect(host=dbhost,
#				database=dbnameto,
				user=dbuser,
				password=dbpass)
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print ("HDB++: wrong username or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print ("HDB++: database not existing")
		else:
			print ("HDB++: " + err)
		hdbpp.close()
		return

	try:
		print ("-----------------------------------------\nUpdate att_conf & error_desc on " + dbhost + "." + dbnamefrom + " -> " + dbhost + "." + dbnameto + "\n-----------------------------------------\n")
		if not options.verbose :
			hdbppcursor = hdbpp.cursor(named_tuple=True, buffered=True)

		sql=updateAttConfErrorDescQuery % (dbnameto,dbnamefrom
		,dbnameto,dbnamefrom
		)
		print sql
		if not options.verbose :
			# executing cursor with execute method and pass SQL query
			for result in hdbppcursor.execute(sql, multi=True):
				if result.with_rows:
					print("Rows produced by statement '{}':".format(result.statement))
					print(result.fetchall())
				else:
					print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))

			hdbpp.commit()
			hdbppcursor.close()

		print("---------> Success\n\n")
	except mysql.connector.Error as err:
	#except Exception as e:
		print("---------> Warn: ", err.msg)
		print("\n\n-------------------------------------------------\n\n")
		return

	hdbpp.close()

def test(dbhost, dbname, dbuser, dbpass):
	hdbpp=mysql.connector.MySQLConnection()
	try:
		if not options.verbose :
			hdbpp = mysql.connector.connect(host=dbhost,
#				database=dbnameto,
				user=dbuser,
				password=dbpass)
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print ("HDB++: wrong username or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print ("HDB++: database not existing")
		else:
			print ("HDB++: " + err)
		hdbpp.close()
		return

	try:
		print ("-----------------------------------------\nTEST on " + dbhost + "." + dbname + "\n-----------------------------------------\n")
		if not options.verbose :
			hdbppcursor = hdbpp.cursor(named_tuple=True, buffered=True)

		sql=testQuery % (dbname)
		print sql
		if not options.verbose :
			# executing cursor with execute method and pass SQL query
			#hdbppcursor.execute(sql, multi=True)
			hdbppcursor.execute(sql)
			#hdbpp.commit()
			print "---------> %d rows\n\n" % hdbppcursor.rowcount
			for row in hdbppcursor:
				print 'Found %d -> %s' % (row.att_conf_id, row.att_name)
			hdbppcursor.close()

		print("---------> Success\n\n")
	except mysql.connector.Error as err:
	#except Exception as e:
		print("---------> Warn: ", err.msg)
		print("\n\n-------------------------------------------------\n\n")
		return

	hdbpp.close()

def main(options):

	#reorganize_future(options.hostarchive,options.dbarchive,options.user,dbpassword,options.year)

	#reorganize_future(options.host,options.db,options.user,dbpassword,options.year)

	#exchange_past(options.hostarchive,options.db,options.dbarchive,options.user,dbpassword,options.year-3)

	#reorganize_past(options.host,options.db,options.user,dbpassword,options.year-3)

	update_att_conf_error_desc(options.hostarchive,options.db,options.dbarchive,options.user,dbpassword)

	#test(options.hostarchive,options.db,options.user,dbpassword)
	#test(options.hostarchive,options.dbarchive,options.user,dbpassword)

if __name__ == '__main__':

	parser = OptionParser()
	parser.add_option("-H", "--host", action = "store", type = "string", dest = "host",
		help = "MySQL Server Address (srv-log-srf-02)")
	parser.add_option("-A", "--hostarchive", action = "store", type = "string", dest = "hostarchive",
		help = "MySQL Server Archive Address (fcslog-replica-01)")
	parser.add_option("-d", "--database", action = "store", type = "string", dest = "db",
		help = "MySQL DB name (hdbpp)")
	parser.add_option("-a", "--databasearchive", action = "store", type = "string", dest = "dbarchive",
		help = "MySQL DB Archive name (hdbpparchive)")
	parser.add_option("-u", "--user", action = "store", type = "string", dest="user",
		help = "MySQL User Id (root)")
	parser.add_option("-y", "--year", action = "store", type = "int", dest="year",
		help = "Year to manage (next year)")
	parser.add_option("-v", "--verbose", action = "store_true", dest="verbose", default=False, help = "Only print query")

	(options, args) = parser.parse_args()
	dbpassword = getpass.getpass("MySQL password for user " + str(options.user) + " :")
	#print (options)
	#print ("database : ", options.db)
	#print (args)
	main(options)
