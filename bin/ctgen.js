#! /usr/bin/env node

var ctgen = require('../lib/main'),
  program = require('commander'),
  package = require('../package');

program
  .version(package.version)

program.command('install')
  .alias('i')
  .description('download and generate database')
  .option('-d, --db [database]', 'database name')
  .option('-v, --verbose', 'verbose')
  .option('-u, --user [user]', 'user')
  .option('-p, --password [pwd]', 'password')
  .option('--authdb [authdb]', 'authdb')
  .option('--no-download','noDownload')
  .option('--no-mongo','noMongo')
  .action(function(options){
    program.runOnce = true;
    if(!options.db){
      options.help && options.help() || program.help();
    };
    ctgen.noDownload = options.noDownload;
    ctgen.noMongo = options.noMongo;
    ctgen.verbose = options.verbose;

    if(ctgen.verbose){
      console.log("use db", options.db);
    };

    if(options.user && options.password){
      console.log("user: ", options.user);
      console.log("password: ", options.password);
      if(options.authdb){
        console.log("authdb: "+options.authdb);
        var authdb = options.authdb;
      }else{
        console.log("authdb: "+options.db);
        var authdb = options.db;
      }
      ctgen.authString = '-u ' + options.user + ' -p "' + options.password + '" --authenticationDatabase ' + options.db;
    }else{
      ctgen.authString = '';
    }

    ctgen.install();

  });

program.
  command('debug')
  .description('debug auth')
  .option('-u, --user [user]', 'user')
  .option('-p, --password [pwd]', 'password')
  .option('-d, --db [database]', 'database name')
  .action(function(options){
    program.runOnce = true;
    ctgen.verbose = true;
    console.log(options.user, options.password);
    if(options.user && options.password){
      ctgen.authString = '-u ' + options.user + ' -p "' + options.password + '" --authenticationDatabase ' + options.db;
    }else{
      ctgen.authString = '';
    }
    ctgen.runDebug(options.db);
  });

program
  .parse(process.argv)


if(!program.runOnce){
  program.help();
}
