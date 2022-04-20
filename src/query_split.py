def query_split(Q,F):
    NQ = [Q]
    for key in F:
        NQ = _apply_filter(NQ,key,F[key])
    return NQ

def _apply_filter(Q,key,values): 
    NQ = []
    for query in Q:
        for chunk in values:
            NQ.append(query.replace('%'+ key + '%',','.join(map(str, chunk))))
    return NQ


def main():

    query = 'SELECT * FROM TABELA1 WHERE field1 IN (%field1%) AND field2 IN (%field2%) AND field3 IN (%field3%)'
    filter = []

    filter.append({'field1': [[1,2,3,4,5,6,7,8,9,10]], 
                   'field2': [[1,2,3,4,5,6,7,8,9,10]], 
                   'field3': [[10,20,30],[40,50,60,70],[88,90,100]]
                  })

    filter.append({'field1': [[1,2,3],[4,5,6],[7,8,9]], 
                   'field2': [[1,2,3,4,5,6,7,8,9,10]], 
                   'field3': [[10,20,30],[40,50,60,70],[88,90,100]]
                  })

    filter.append({'field1': [[1,2,3],[4,5,6],[7,8,9]], 
                   'field2': [[1,2,3],[4,5,6],[7],[8,9,10],[13,14,15]], 
                   'field3': [[10,20,30],[40,50,60,70],[88,90,100]]
                  })



    for f in filter:
        print("----------------" + str(f) + "------------------")
        print(*query_split(query,f), sep = "\n")



main()