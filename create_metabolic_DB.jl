#!/usr/bin/env julia
#=
@name: create_metabolic_DB.jl
@author: Juan C. Castro <jccastrog at gatech dot edu>
@update: 15-Jan-2018
@version: 1.0.4
@license: GNU General Public License v3.0.
please type "./fitModel.py -h" for usage help
=#

###===== 1.0 Load packages, define functions, initialize variables =====###
using ArgParse
using MySQL
using ConfParser

function parse_commandline()
    s = ArgParseSettings()

    @add_arg_table s begin
        "--reactions_file", "-r"
            help = "A table  with metabolic reactions"
			required = true
        "--compounds_file", "-c"
            help = "A table with metabolic compounds"
			required = true
		"--database_conf", "-d"
			help = "A configuraton file for the database"
			required = true
        "--index"
            help = "If present reactions and compounds will be added to the database"
            action = :store_true
    end

    return parse_args(s)
end

function manipulate_db(configFile, operation, values)
    conf = ConfParse(configFile)
    parse_conf!(conf)
    user = retrieve(conf, "database", "USER")
    password = retrieve(conf, "database", "PASSWORD")
    port = retrieve(conf, "database", "PORT")
    host     = retrieve(conf, "database", "HOST")
    socket = retrieve(conf, "database", "SOCKET")
    db=retrieve(conf, "database", "DB")
    conn = MySQL.connect(host, user, password; db=db, port=port, opts = Dict())
    sqlInsert = "INSERT INTO reactions"
    MySQL.Stmt(conn, "INSERT INTO reactions (")
    if operation=="insertReaction"
        sqlInsert = "INSERT INTO reactions (id, direction, compartment, name, deltaG, reference, equation, equation_metnames, bigg_id, kegg_id, kegg_pathway, metacyc_pathway)"
        sqlValues = values
        sql = "$sqlInsert $sqlValues
        MySQL.execute!(conn, sql)
    end



end

function reation_insert()

function parse_reaction_file(reactionFile, configFile)
    rFile = open(reactionFile);
    for line in eachline(rFile);
        line = rstrip(line);
        fields = split(line,"\t");
        ID = split(fields[1], "_")[1]
        #ID, compartment = split(ID,"_")
        direction = fields[2]
        compartment = fields[3]
        gpr = fields[4]
        name = fields[5]
        enzyme = fields[6]
        deltag = fields[7]
        reference = fields[8]
        equation = fields[9]
        equationMetnames = fields[10]
        try
            biggID = fields[11]
            catch
            biggID = "NULL"
        end
        try
            keggID = fields[12]
        catch
            keggID = "NULL"
        end
        try
            keggPathways = fields[13]
        catch
                keggPathways = "NULL"
        end
        try
            metacyc_parthways = fields[14]
        catch
            metacyc_parthways = "NULL"
        end
    end
    sqlValues = "VALUES ($id, $direction, $compartment, $name, $deltag, $reference, $equation, $equationMetnames, $biggID, $keggID, $keggPathway, $metacycPathway);"
    manipulate_db(configFile, "insert_reaction", sqlValues)
    MySQL.execute!(conn, sql)
    close(rFile)
end

function main()
    parsedArgs = parse_commandline();
    reactionFile = parsedArgs["reactions_file"]
    database_conf = parsedArgs["database_conf"]
	parse_reaction_file(reactionFile)
    manipulate_db(database_conf,"asd")
end

main()
write(STDOUT,"Hello World\n")
