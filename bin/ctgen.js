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
  .option('--xlsx [path]','xls files to process')
  .option('--csv [path]','csv files to process')
  .option('--no-mongo','noMongo')
  .option('--aws-id [n]', 'Amazon ID', null)
  .option('--aws-secret [n]', 'Amazon Secret', null)
  .option('--aws-region [n]', 'Amazon Region',null )
  .option('--aws-bucket [n]', 'remote bucket', null)
  .option('--aws-dir [n]', 'amazon bucket dir', null)
  .option('--only-process','only run scripts for process data in db')
  .option('--run','run in this process')
  .option('--spawn', 'run in separate processes')
  .action(function(options){
    program.runOnce = true;
    options.noMongo = !options.mongo;
    if(!options.db && !options.noMongo){
      options.help && options.help() || program.help();
      return;
    };

    if(options.awsId || options.awsSecret || options.awsRegion || options.awsBucket || options.awsDir) {
      if(options.awsId === null || options.awsSecret === null || options.awsRegion === null || options.awsDir === null || options.awsBucket === null) {
        options.help && options.help() || program.help();
        return
      } else {
        options.aws = {
          id: options.awsId,
          secret: options.awsSecret,
          region: options.awsRegion,
          bucket: options.awsBucket,
          dir: options.awsDir,
        }
      console.log("OPTIONS", options.aws)
        
      }
    }
    ctgen.verbose = options.verbose;

    if(!options.noMongo){
      console.log("use db", options.db);
    };

    options.authString = '';
    if(options.user && options.password){
      options.authString = formatAuthString(options);
    }

    ctgen.install(options);

  });

program.
  command('debug')
  .description('debug auth')
  .option('-u, --user [user]', 'user')
  .option('-p, --password [pwd]', 'password')
  .option('-d, --db [database]', 'database name')
  .option('--authdb [authdb]', 'authdb')
  .option('--run', 'run command')
  .action(function(options){
    program.runOnce = true;
    ctgen.verbose = true;

    options.authString = '';
    if(options.user && options.password){
      options.authString = formatAuthString(options);
    }
    ctgen.runDebug(options);
  });

program
  .parse(process.argv);


if(!program.runOnce){
  program.help();
}

function formatAuthString(options) {
  return '-u ' + options.user + ' -p "' + options.password + '" --authenticationDatabase ' + (options.authdb || options.db);
}
