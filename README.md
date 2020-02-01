target schedule Q1 2020

## Manufacturing Execution System:  
-completely written in Python  
-order queue provided by an SQLite3 database  
-order distribution via OPC UA method  
-order quality assurance report  
-order prioritization  
-reintegration of faild orders into the queue   
-...   
  
### ERP -> PPS (MySQL-Server, slow network based) -> MES (SQLite3 queue, fast filebased and closer to shopfloor) -> one ore may PLC  
