import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, Response
import psycopg2

app = Flask(__name__)

def get_db_connection():

    load_dotenv()

    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        database=os.getenv('POSTGRES_DB'),
        port=os.getenv('POSTGRES_PORT'),
        user=os.getenv('POSTGRES_USERNAME'),
        password=os.getenv('POSTGRES_PASSWORD'))

    return conn


@app.route('/imports', methods=['POST'])
def imports():
    try:
        
        conn = get_db_connection()
        cur = conn.cursor()


        content = request.json
        item_date = content["updateDate"]
        for item in content["items"]:
            item_type = item["type"]
            try:
                item_url = "'" + str(item["url"]) + "'"
            except:
                item_url = "NULL"
            item_id = item["id"]
            try:
                item_size = str(item["size"])
            except:
                item_size = "NULL"
            try:
                item_parentId = item["parentId"]
                if item_parentId == None:
                    item_parentId = "NULL"
                else:
                    item_parentId = "'" + item_parentId + "'"
            except:
                item_parentId = "NULL"
                
            # print(item_type, item_url, item_id, item_size, item_parentId, item_date)

            query = ("INSERT INTO files (type, url, id, size, parentId, date) \
                    VALUES ('%s', %s, '%s', %s, %s, '%s')" % \
                    (item_type,
                    item_url,
                    item_id,
                    item_size,
                    item_parentId,
                    item_date))
            cur.execute(query)
            query = ("UPDATE files \
                    SET children = array_append(children, '%s') \
                    WHERE id = %s" % \
                    (item_id,
                    item_parentId))
            cur.execute(query)
            if item_parentId != "NULL":
                update_parents_date(item_parentId, item_date, cur)
        conn.commit()
        cur.close()
        conn.close()
        data = {
            "code" : 200,
        }
        return jsonify(data), 200
    except:
        data = {
            "code" : 400,
            "message": "Validation Failed",
        }
        return jsonify(data), 400

def update_parents_date(item_parentId, item_date, cur):
    
    if item_parentId[0] != "'":
        item_parentId = "'"+item_parentId+"'"
    query = ("UPDATE files \
            SET date = '%s' \
            WHERE id = %s" % \
            (item_date,
            item_parentId))
    cur.execute(query)
    query = ("SELECT parentId FROM files WHERE id = " + item_parentId)
    cur.execute(query)
    items = cur.fetchall()
    item_parentId = items[0][0]
    if not item_parentId:
        return
    update_parents_date(item_parentId, item_date, cur)


@app.route('/nodes/<id>')
def nodes(id=None):
    result, _ = info(id)
    if result == "Error" :
        data = {
            "code": 400,
            "message": "Validation Failed",
        }
        return jsonify(data), 400
    if result is None:
        data = {
            "code": 404,
            "message": "Item not found",
        }
        return jsonify(data), 404

    return result, 200

def info(id):
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = ("SELECT * FROM files WHERE id = '" + id + "'")
        cur.execute(query)
        items = cur.fetchall()
        if items == []:
            return None, 0
        else:
            item = items[0]
            item_type = item[0]
            item_url = item[1]
            item_id = item[2]
            item_size = item[3]
            item_parentId = item[4]
            item_date = item[5]
            item_childrens = item[6]
            childrens_list = []
            for children in item_childrens:
                my_children, children_size = info(children)
                childrens_list.append(my_children)
                if children_size is not None:
                    if item_size is not None:
                        item_size += children_size
                    else:
                        item_size = children_size

            if item_type == "FILE":
                if not len(childrens_list):
                    childrens_list = None
            
            # print(item_type, item_url, item_id, item_size, item_parentId, item_date, childrens_list)

            result = {
                "type": item_type,
                "url": item_url,
                "id": item_id,
                "size": item_size,
                "parentId": item_parentId,
                "date": item_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "children": childrens_list
            }
        cur.close()
        conn.close()
        return result, item_size

    except:
        return "Error", 0


@app.route('/delete/<id>', methods=["DELETE"])
def delete(id=None):
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        query = ("SELECT parentId FROM files WHERE id = '" + id +"'")
        cur.execute(query)
        parId = cur.fetchall()
        parentId = parId[0][0]
        if parentId:
            parentId = "'"+parId[0][0]+"'"
        delete_category(id, cur)
        if parentId:
            # delete id from parent's children_list
            query = ("UPDATE files \
                    SET children = array_remove(children, '%s') \
                    WHERE id = %s" % \
                    (id,
                    parentId))
            cur.execute(query)
    except:
        return "Error", 404

    conn.commit()
    cur.close()
    conn.close()

    return "Ok", 200

def delete_category(id, cur):

    if id[0] != "'":
        id = "'"+id+"'"
    query = ("SELECT children FROM files WHERE id = " + id)
    cur.execute(query)
    items = cur.fetchall()
    if len(items) == 0:
        raise ValueError('No id found')

    items = items[0][0]

    if len(items) != 1 or items != []:
        for item in items:
            delete_category(item, cur)
    
    query = ("DELETE FROM files WHERE id = " + id)
    return cur.execute(query)



if __name__ == '__main__':
    app.run(host='0.0.0.0')
