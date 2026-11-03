from database.DB_connect import DBConnect
from model.Constructor import Constructor
class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(anno1, anno2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT c.*
FROM constructors c, results r, races ra
WHERE c.constructorId = r.constructorId
AND r.raceId = ra.raceId
AND ra.year BETWEEN %s AND %s
AND r.position IS NOT NULL"""

        cursor.execute(query, (anno1, anno2))

        for row in cursor:
            results.append(Constructor(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(anno1, anno2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.IDconstractor as id1, t2.IDconstractor as id2, COUNT(DISTINCT t1.IDdriver) as peso
FROM
(SELECT c.constructorId as IDconstractor, r.driverId as IDdriver, r.raceId as IDrace
FROM constructors c, results r, races ra
WHERE c.constructorId = r.constructorId
AND r.raceId = ra.raceId
AND ra.year BETWEEN %s AND %s
AND r.position IS NOT NULL) t1,
(SELECT c.constructorId as IDconstractor, r.driverId as IDdriver, r.raceId as IDrace
FROM constructors c, results r, races ra
WHERE c.constructorId = r.constructorId
AND r.raceId = ra.raceId
AND ra.year BETWEEN %s AND %s
AND r.position IS NOT NULL) t2
WHERE t1.IDconstractor < t2.IDconstractor
AND t1.IDdriver = t2.IDdriver
AND t1.IDrace != t2.IDrace
GROUP BY t1.IDconstractor, t2.IDconstractor"""

        cursor.execute(query, (anno1, anno2, anno1, anno2))

        for row in cursor:
            results.append((row["id1"], row["id2"], row["peso"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getConstrutorOldest():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT c.constructorId as idC, MIN(d.dob) as minYaer
FROM constructors c, results r, drivers d 
WHERE c.constructorId = r.constructorId
AND r.driverId = d.driverId
GROUP BY c.constructorId"""

        cursor.execute(query)

        for row in cursor:
            results.append((row["idC"], row["minYaer"]))

        cursor.close()
        conn.close()
        return results

