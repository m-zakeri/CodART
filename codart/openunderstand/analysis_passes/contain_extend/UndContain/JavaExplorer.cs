using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Antlr4.Runtime;
using Dapper;
using Microsoft.Data.Sqlite;

namespace UndContain;

public class JavaExplorer
{
    public JavaExplorer(string projectPath)
    {
        ProjectPath = projectPath;
        JavaFiles = Directory.EnumerateFiles(projectPath, "*.java", SearchOption.AllDirectories).ToList();
    }

    private string ProjectPath { get; }
    private IEnumerable<string> JavaFiles { get; }
    private List<JavaEntity> Entities { get; } = new();
    private List<JavaReference> References { get; } = new();

    public void ExplorePackages(string[] refs)
    {
        JavaPackageVisitor visitor = new();

        foreach (var file in JavaFiles)
        {
            var stream = CharStreams.fromPath(file);
            var lexer = new JavaLexer(stream);
            var tokens = new CommonTokenStream(lexer);
            JavaParserLabeled parser = new(tokens)
            {
                BuildParseTree = true
            };
            var tree = parser.compilationUnit();
            visitor.Visit(tree);
        }

        Entities.AddRange(visitor.ExtractEntities());
        References.AddRange(visitor.ExtractReferences(refs));

        Console.WriteLine("exploration done!");
    }

    public void ExportToDb(string sqliteConnectionString)
    {
        using var con = new SqliteConnection(sqliteConnectionString);

        var rowCount =
            con.Execute(
                "insert or ignore into entitymodel (_id, _kind_id, _parent_id, _name, _longname, _value, _type, _contents)" +
                "VALUES (@Id, (select k._id from kindmodel k where k._name = @Kind), @ParentId, @Name, @LongName, null, null, @Contents)",
                Entities);

        Console.WriteLine($"added {rowCount} rows into entitymodel");

        rowCount =
            con.Execute(
                "insert or ignore into referencemodel (_id, _kind_id, _file_id, _line, _column, _ent_id, _scope_id)" +
                "VALUES (@Id, (select k._id from kindmodel k where k._name = @Kind), @FileId, @Line, @Column, @EntId, @ScopeId)",
                References);

        Console.WriteLine($"added {rowCount} rows into referencemodel");
    }
}