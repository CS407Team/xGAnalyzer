<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title> Login Page </title>
<style>
    Body {
        font-family: Calibri, Helvetica, sans-serif;
        font-size: xx-large;
        background-color: darkblue;
    }
    h1 {
        position: relative;
        color: grey;
    }
    h2 {
        font-size: medium;
        color: lightgray;
    }
    .header{
        padding-left: 100px;
    }
    .header img {
        float: left;
        width: 500px;
        height: 300px;
    }
    label {
        color: whitesmoke;
    }
    button {
       background-color: #4CAF50;
       width: 44%;
       color: yellow;
       padding: 15px;
       margin: 10px 0px;
       border: none;
       cursor: pointer;
       font-size: large;
    }
    form {
        border-left: 100px solid #0096FF;
        border-right: 100px solid #0096FF;
        border-top: 5px solid #0096FF;
        border-bottom: 5px solid #0096FF;
    }
    input[type=text], input[type=password] {
        width: 50%;
        margin: 8px 0;
        padding: 12px 20px;
        display: inline-block;
        border: 2px solid green;
        box-sizing: border-box;
    }
    button:hover {
        opacity: 0.7;
    }
    .cancelbtn {
        width: auto;
        padding: 10px 18px;
        margin: 10px 5px;
    }
    .container {
        padding: 25px;
        background-color: lightblue;
        color: whitesmoke;
    }
</style>
</head>
<body>
    <div class="header">
    <img src="https://i.ibb.co/K7K5D49/xgGraph.png" alt="logo" />
    <h1>&ensp;xG Analyzer</h1>
    </div>
      <h2>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; We analyze, you decide </h2>
    <br><br><br><br>
    <form method="POST" action="signup.php">
        <div class="container">
            <label>Choose Username : </label>
            <input type="text" placeholder="&ensp;Enter Your Username" name="susername" required>
            <br><label>Choose Password :&nbsp;</label>
            <input type="password" placeholder="&ensp;Enter Your Password" name="spassword" required>
            <br><label>Enter Your Email :&nbsp;</label>
            <input type="text" placeholder="&ensp;Enter Your Email" name="semail" required>
            <br><label>Enter First Name :&nbsp;</label>
            <input type="text" placeholder="&ensp;Enter First Name" name="sfirstname" required>
            <br><label>Enter Last Name :&nbsp;</label>
            <input type="text" placeholder="&ensp;Enter Last Name" name="slastname" required>
            <br><button type="submit" action="signup.php">Sign Up</button>
        </div>
    </form>
</body>
</html>


