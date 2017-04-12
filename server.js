var express = require('express');
var app = express();
var d = {};
var passport = require('passport');
var SpotifyStrategy = require('passport-spotify').Strategy;
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var methodOverride = require('method-override');

// express, npm
app.use(express.static(__dirname));
app.use(express.static(__dirname+'/styles.css'));
app.get('/Bitcamp.html', function (req, res) {
    var cookie = req.cookies;
    if (cookie.auth_code === undefined) {
        res.redirect('/auth');
    } else {
        res.sendFile( __dirname + "/" + "Bitcamp.html" );
    }

})

// spotify
// Passport session setup.
//   To support persistent login sessions, Passport needs to be able to
//   serialize users into and deserialize users out of the session. Typically,
//   this will be as simple as storing the user ID when serializing, and finding
//   the user by ID when deserializing. However, since this example does not
//   have a database of user records, the complete spotify profile is serialized
//   and deserialized.
passport.serializeUser(function(user, done) {
  done(null, user);
});

passport.deserializeUser(function(obj, done) {
  done(null, obj);
});

// Use the SpotifyStrategy within Passport.
//   Strategies in Passport require a `verify` function, which accept
//   credentials (in this case, an accessToken, refreshToken, and spotify
//   profile), and invoke a callback with a user object.
passport.use(new SpotifyStrategy({
  clientID: "5182a98e4c0742f78fe0f764ebeaab97",
  clientSecret: "dcc81899e59c4a2daa0cf92affc64760",
  callbackURL: "http://sample-env-2.tgmsm5cyvt.us-west-2.elasticbeanstalk.com/callback/"
   },
  function(accessToken, refreshToken, profile, done) {
    // asynchronous verification, for effect...

        console.log("tokens");
        console.log(profile);
        console.log(refreshToken);
    process.nextTick(function () {
      // To keep the example simple, the user's spotify profile is returned to
      // represent the logged-in user. In a typical application, you would want
      // to associate the spotify account with a user record in your database,
      // and return that user instead.
      return done(null, {token:accessToken,user:profile});
    });
  }));

app.set('view engine', 'ejs');
app.use(cookieParser());
app.use(cookieParser());
app.use(methodOverride());

app.use(passport.initialize());
app.use(passport.session());


app.get('/', function(req,res){
    var cookie = req.cookies;
    if (cookie.auth_code === undefined) {
        res.redirect('/auth');
    } else {
        res.redirect('/Bitcamp.html');
    }
})

// GET /auth/spotify
//   Use passport.authenticate() as route middleware to authenticate the
//   request. The first step in spotify authentication will involve redirecting
//   the user to spotify.com. After authorization, spotify will redirect the user
//   back to this application at /auth/spotify/callback
app.get('/auth',
  passport.authenticate('spotify', {scope: ['playlist-modify-public', 'playlist-modify-private'], showDialog: true}),
  function(req, res){
// The request will be redirected to spotify for authentication, so this
// function will not be called.
});

// GET /auth/spotify/callback
//   Use passport.authenticate() as route middleware to authenticate the
//   request. If authentication fails, the user will be redirected back to the
//   login page. Otherwise, the primary route function function will be called,
//   which, in this example, will redirect the user to the home page.
app.get('/callback',
  passport.authenticate('spotify', { failureRedirect: '/oops.html' }),
  function(req, res) {
      console.log(req);
      console.log(req.user.token);
      console.log(req.user.user.id);
      res.cookie("auth_code",req.user.token,{maxAge : 1000*3600});
      res.cookie("name",req.user.user.id,{maxAge : 1000*3600});
      res.redirect('/');
  });


app.get('/events', function (req, res) {
   console.log("Getting Events Now");
   if (typeof req.query.artist != 'undefined') {
       // GET THE EVENT ID(S) TO GET ARTISTS FOR
       var artist = req.query.artist;
       var startdate = req.query.startdate;
       var enddate = req.query.enddate;

       console.log(req.query);

       console.log(artist);


       // PYTHON SCRIPT TO GET ARTISTS FROM EVENT IDS
       var spawn = require("child_process").spawn;
       var process = spawn('python',["BACKENDartists2events.py", artist,startdate,enddate]);

       str = {data:""}

       process.stdout.on('data', function (data){
           // GET THE DATA
            str.data += data.toString();
       });

       process.on('close', function(code) {
            // RENDER OUR EMBEDDED JAVASCRIPT WITH OUR JSON DATA
            response = JSON.parse(str.data);
            res.end(JSON.stringify(response));
        });
   } else {
       console.log("From Venue");
       var venue = req.query.venue;
       var startdate = req.query.startdate;
       var enddate = req.query.enddate;

       console.log("Run Python");
       // RUN OUR PYTHON SCRIPT
       var spawn = require("child_process").spawn;
       // SCRIPT TO TURN A VENUE ID INTO EVENTS GIVEN START DATE AND END DATE
       var process = spawn('python',["BACKENDvenue2events.py", venue, startdate, enddate]);

       console.log("Python In prog");
       // OBJECT TO STORE DATA
       str = {data:""}

       // BUFFER MAY BE TOO SMALL, SO THIS INNER FUNCTION MAY BE CALLED MULTIPLE TIMES
        process.stdout.on('data', function (data){
            // WHEN DATA IS RECEIVED IN THE BUFFER, ADD IT TO THE STR OBJECT
            console.log("Data received");
            console.log(str.data.length)
            str.data += data.toString()
        });

       // WHEN OUR PYTHON SCRIPT FINISHES
        process.on('close', function(code) {
            console.log("Data done");
            // GET OUR JSON RESPONSE READY
           var response = {
              venue:venue,
              data:JSON.parse(str.data)
           };
           console.log("Render Data ");
           // RETURN OUR JSON RESPONSE

           res.end(JSON.stringify(response));


        });
   }

})

app.get('/artists', function (req, res) {

   // GET THE EVENT ID(S) TO GET ARTISTS FOR
   var event_ids = req.query.event_ids;


   console.log(req.query);

   console.log(event_ids);

   // PYTHON SCRIPT TO GET ARTISTS FROM EVENT IDS
   var spawn = require("child_process").spawn;
   var process = spawn('python',["BACKENDevents2artists.py", event_ids]);

   str = {data:""}

   process.stdout.on('data', function (data){
       // GET THE DATA
        str.data += data.toString();
   });

   process.on('close', function(code) {
        // RENDER OUR EMBEDDED JAVASCRIPT WITH OUR JSON DATA
       res.render('ConcertInfo', { artists: JSON.parse(str.data) });

    });


})

app.get('/playlist', function (req, res) {

   // GET THE EVENT ID(S) TO GET ARTISTS FOR
   var artist_ids = req.query.artists;

   console.log(req.query);

   console.log(req.cookies.auth_code);

   // PYTHON SCRIPT TO GET ARTISTS FROM EVENT IDS
   var spawn = require("child_process").spawn;
   var process = spawn('python',["BACKENDartists2playlist.py",artist_ids,req.cookies.auth_code,req.cookies.name]);

   // Store the to-be playlist URL
   str = {data:""}

   process.stdout.on('data', function (data){
       // GET THE DATA
        str.data += data.toString();
   });

   // When the playlist is created, redirect to the playlist link
   process.on('close', function(code) {
        // REDIRECT TO PLAYLIST
        console.log(str.data);
       res.redirect(str.data);

    });


})
//var server = app.listen(process.env.PORT, function ()
var server = app.listen(process.env.PORT, function () {
   var host = server.address().address
   var port = server.address().port
   console.log("Example app listening at http://%s:%s", host, port)

})

// Simple route middleware to ensure user is authenticated.
//   Use this route middleware on any resource that needs to be protected.  If
//   the request is authenticated (typically via a persistent login session),
//   the request will proceed. Otherwise, the user will be redirected to the
//   login page.
function ensureAuthenticated(req, res, next) {
  if (req.isAuthenticated()) { return next(); }
  res.redirect('/login');
}
