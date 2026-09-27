var mysql = require('mysql');
var con = mysql.createConnection({
  host: "54.202.2.104",
  user: "test",
  password: "9874123650"
});

con.connect(function(err) {
  console.log("Connected!");
  con.query("SELECT * FROM Famous_Lives.test_table", function (err, result,fields) {    
  	console.log("err:"+err);
    console.log(result[0].PersonID);
    con.end();
  });
});
