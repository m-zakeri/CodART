using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Antlr4.Runtime;
using Antlr4.Runtime.Misc;
using Antlr4.Runtime.Tree;

namespace UndContain;

public class JavaPackageVisitor : JavaParserLabeledBaseVisitor<string>
{
    private int _lastEntityId;
    private int _lastReferenceId;
    private int NewEntityId => ++_lastEntityId;
    private int NewReferenceId => ++_lastReferenceId;
    private List<JavaTypeDeclaration> JavaTypeDeclarations { get; } = new();
    private List<JavaEntity> JavaEntities { get; } = new();
    private List<JavaReference> JavaReferences { get; } = new();

    public override string VisitCompilationUnit(JavaParserLabeled.CompilationUnitContext context)
    {
        var package = context
            .children
            .OfType<JavaParserLabeled.PackageDeclarationContext>()
            .FirstOrDefault();

        var packageName = package?.children
            .OfType<JavaParserLabeled.QualifiedNameContext>()
            .Select(p => p.GetText())
            .First();

        if (packageName is null)
            return "";

        JavaTypeDeclarations.AddRange(GetDeclarations(context, packageName));

        return packageName;
    }

    private IEnumerable<JavaTypeDeclaration> GetDeclarations(
        IParseTree context,
        string packageName)
    {
        if (context is not ParserRuleContext ruleContext)
            yield break;

        foreach (var child in ruleContext.children)
        {
            var declarations = child switch
            {
                null => Enumerable.Empty<JavaTypeDeclaration>(),

                JavaParserLabeled.ImportDeclarationContext c
                    => GetImportDeclarations(c, packageName),

                JavaParserLabeled.TypeDeclarationContext c
                    when c.children.OfType<JavaParserLabeled.ClassDeclarationContext>().Any()
                    => GetClassDeclarations(c, packageName),

                JavaParserLabeled.TypeDeclarationContext c
                    when c.children.OfType<JavaParserLabeled.InterfaceDeclarationContext>().Any()
                    => GetInterfaceDeclarations(c, packageName),

                JavaParserLabeled.TypeDeclarationContext c
                    when c.children.OfType<JavaParserLabeled.EnumDeclarationContext>().Any()
                    => GetEnumDeclarations(c, packageName),

                JavaParserLabeled.TypeDeclarationContext c
                    when c.children.OfType<JavaParserLabeled.AnnotationTypeDeclarationContext>().Any()
                    => GetAnnotationTypeDeclarations(c, packageName),

                _ => GetDeclarations(child, packageName)
            };

            foreach (var declaration in declarations)
            {
                yield return declaration;
            }
        }
    }

    private IEnumerable<JavaTypeDeclaration> GetImportDeclarations(
        JavaParserLabeled.ImportDeclarationContext context, string packageName)
    {
        if (context.children.All(cc => cc.GetText() != "*"))
        {
            var importChunks = context.qualifiedName().GetText().Split('.');

            yield return new JavaTypeDeclaration
            {
                Kind = JavaTypeDeclarationKind.FromImport,
                PackageName = string.Join('.', importChunks[..^1]),
                Modifier = "",
                Name = importChunks[^1],
                Content = "",
                Line = context.Start.Line,
                Column = context.Start.Column,
                FilePath = context.Start.InputStream.SourceName
            };
        }

        foreach (var declaration in context.children.SelectMany(c => GetDeclarations(c, packageName)))
        {
            yield return declaration;
        }
    }

    private IEnumerable<JavaTypeDeclaration> GetClassDeclarations(
        JavaParserLabeled.TypeDeclarationContext context, string packageName)
    {
        var extendTokens = context.children
            .OfType<JavaParserLabeled.ClassDeclarationContext>()
            .First()
            .children
            .OfType<JavaParserLabeled.TypeTypeContext>()
            .FirstOrDefault()?
            .children
            .OfType<JavaParserLabeled.ClassOrInterfaceTypeContext>()
            .FirstOrDefault()?
            .GetTokens(JavaLexer.IDENTIFIER)
            .Select(it => it.GetText())
            .ToArray();

        var cDeclaration = new JavaTypeDeclaration
        {
            Kind = JavaTypeDeclarationKind.Class,
            PackageName = packageName,
            Modifier =
                string.Join(' ',
                    context.children
                        .OfType<JavaParserLabeled.ClassOrInterfaceModifierContext>()
                        .Where(m => m.GetType() != typeof(JavaParserLabeled.AnnotationContext))
                        .Select(m => m.GetText())),

            Name =
                context.children
                    .OfType<JavaParserLabeled.ClassDeclarationContext>()
                    .First()
                    .IDENTIFIER()
                    .GetText()!,

            Content = context.Start.InputStream.GetText(new Interval(context.Start.StartIndex, context.Stop.StopIndex)),
            Line = context.Start.Line,
            Column = context.Start.Column,
            FilePath = context.Start.InputStream.SourceName,
            Extends = extendTokens is null ? null : new[] {string.Join('.', extendTokens)}
        };

        yield return cDeclaration;

        foreach (var declaration in context.children.SelectMany(c => GetDeclarations(c, packageName)))
        {
            yield return declaration;
        }
    }

    private IEnumerable<JavaTypeDeclaration> GetInterfaceDeclarations(JavaParserLabeled.TypeDeclarationContext context,
        string packageName)
    {
        var extendTokens = context.children
            .OfType<JavaParserLabeled.InterfaceDeclarationContext>()
            .First()
            .children
            .OfType<JavaParserLabeled.TypeListContext>()
            .FirstOrDefault()?
            .children
            .OfType<JavaParserLabeled.TypeTypeContext>()
            .SelectMany(tt => tt.children.OfType<JavaParserLabeled.ClassOrInterfaceTypeContext>())
            .Select(tt => tt.GetTokens(JavaLexer.IDENTIFIER).Select(it => it.GetText()).ToArray())
            .ToArray();

        yield return new JavaTypeDeclaration
        {
            Kind = JavaTypeDeclarationKind.Interface,
            PackageName = packageName,
            Modifier =
                string.Join(' ',
                    context.children
                        .OfType<JavaParserLabeled.ClassOrInterfaceModifierContext>()
                        .Where(m => m.GetType() != typeof(JavaParserLabeled.AnnotationContext))
                        .Select(m => m.GetText())),

            Name =
                context.children
                    .OfType<JavaParserLabeled.InterfaceDeclarationContext>()
                    .First()
                    .IDENTIFIER()
                    .GetText()!,

            Content = context.Start.InputStream.GetText(new Interval(context.Start.StartIndex, context.Stop.StopIndex)),
            Line = context.Start.Line,
            Column = context.Start.Column,
            FilePath = context.Start.InputStream.SourceName,
            Extends = extendTokens?.Select(et => string.Join('.', et)).ToArray()
        };

        foreach (var declaration in context.children.SelectMany(c => GetDeclarations(c, packageName)))
        {
            yield return declaration;
        }
    }

    private IEnumerable<JavaTypeDeclaration> GetEnumDeclarations(JavaParserLabeled.TypeDeclarationContext context,
        string packageName)
    {
        yield return new JavaTypeDeclaration
        {
            Kind = JavaTypeDeclarationKind.Enum,
            PackageName = packageName,
            Modifier =
                string.Join(' ',
                    context.children
                        .OfType<JavaParserLabeled.ClassOrInterfaceModifierContext>()
                        .Where(m => m.GetType() != typeof(JavaParserLabeled.AnnotationContext))
                        .Select(m => m.GetText())),

            Name =
                context.children
                    .OfType<JavaParserLabeled.EnumDeclarationContext>()
                    .First()
                    .IDENTIFIER()
                    .GetText()!,

            Content = context.Start.InputStream.GetText(new Interval(context.Start.StartIndex, context.Stop.StopIndex)),
            Line = context.Start.Line,
            Column = context.Start.Column,
            FilePath = context.Start.InputStream.SourceName
        };

        foreach (var declaration in context.children.SelectMany(c => GetDeclarations(c, packageName)))
        {
            yield return declaration;
        }
    }

    private IEnumerable<JavaTypeDeclaration> GetAnnotationTypeDeclarations(
        JavaParserLabeled.TypeDeclarationContext context, string packageName)
    {
        yield return new JavaTypeDeclaration
        {
            Kind = JavaTypeDeclarationKind.AnnotationType,
            PackageName = packageName,
            Modifier =
                string.Join(' ',
                    context.children
                        .OfType<JavaParserLabeled.ClassOrInterfaceModifierContext>()
                        .Where(m => m.GetType() != typeof(JavaParserLabeled.AnnotationContext))
                        .Select(m => m.GetText())),

            Name =
                context.children
                    .OfType<JavaParserLabeled.AnnotationTypeDeclarationContext>()
                    .First()
                    .IDENTIFIER()
                    .GetText()!,

            Content = context.Start.InputStream.GetText(new Interval(context.Start.StartIndex, context.Stop.StopIndex)),
            Line = context.Start.Line,
            Column = context.Start.Column,
            FilePath = context.Start.InputStream.SourceName
        };

        foreach (var declaration in context.children.SelectMany(c => GetDeclarations(c, packageName)))
        {
            yield return declaration;
        }
    }

    public IEnumerable<JavaEntity> ExtractEntities()
    {
        JavaEntities.Clear();
        
        var fileEntities =
            JavaTypeDeclarations
                .Select(d => d.FilePath)
                .ToHashSet()
                .Select(f => new JavaEntity
                {
                    Id = NewEntityId,
                    ParentId = null,
                    Name = Path.GetFileName(f),
                    LongName = f,
                    FilePath = f,
                    Contents = File.ReadAllText(f),
                    Kind = "Java File"
                })
                .ToList();

        var knownPackageEntities =
            JavaTypeDeclarations
                .Where(d => d.Kind != JavaTypeDeclarationKind.FromImport)
                .GroupBy(d => d.PackageName)
                .Select(g => g.First())
                .Select(d => new JavaEntity
                {
                    Id = NewEntityId,
                    Name = d.PackageName.Split('.').Last(),
                    LongName = d.PackageName,
                    FilePath = d.FilePath,
                    Contents = null,
                    Package = null,
                    ParentId = fileEntities.First(f => f.FilePath == d.FilePath).Id,
                    Kind = "Java Package"
                })
                .ToList();

        var classEntities =
            JavaTypeDeclarations
                .Where(d => d.Kind == JavaTypeDeclarationKind.Class)
                .Select(d => new JavaEntity
                {
                    Id = NewEntityId,
                    Name = d.Name,
                    LongName = $"{d.PackageName}.{d.Name}",
                    FilePath = d.FilePath,
                    Contents = d.Content,
                    Package = knownPackageEntities.First(p => p.LongName == d.PackageName),
                    ParentId = fileEntities.First(p => p.FilePath == d.FilePath).Id,
                    Kind = EntityKindUtils.GetClassKind(d.Name, d.Modifier),
                    Line = d.Line,
                    Column = d.Column
                })
                .ToList();

        var interfaceEntities =
            JavaTypeDeclarations
                .Where(d => d.Kind == JavaTypeDeclarationKind.Interface)
                .Select(d => new JavaEntity
                {
                    Id = NewEntityId,
                    Name = d.Name,
                    LongName = $"{d.PackageName}.{d.Name}",
                    FilePath = d.FilePath,
                    Contents = d.Content,
                    Package = knownPackageEntities.First(p => p.LongName == d.PackageName),
                    ParentId = fileEntities.First(p => p.FilePath == d.FilePath).Id,
                    Kind = EntityKindUtils.GetInterfaceKind(d.Name, d.Modifier),
                    Line = d.Line,
                    Column = d.Column
                })
                .ToList();

        var enumEntities =
            JavaTypeDeclarations
                .Where(d => d.Kind == JavaTypeDeclarationKind.Enum)
                .Select(d => new JavaEntity
                {
                    Id = NewEntityId,
                    Name = d.Name,
                    LongName = $"{d.PackageName}.{d.Name}",
                    FilePath = d.FilePath,
                    Contents = d.Content,
                    Package = knownPackageEntities.First(p => p.LongName == d.PackageName),
                    ParentId = fileEntities.First(p => p.FilePath == d.FilePath).Id,
                    Kind = EntityKindUtils.GetEnumKind(d.Name, d.Modifier),
                    Line = d.Line,
                    Column = d.Column
                })
                .ToList();

        var interfaceAnnotationEntities =
            JavaTypeDeclarations
                .Where(d => d.Kind == JavaTypeDeclarationKind.AnnotationType)
                .Select(d => new JavaEntity
                {
                    Id = NewEntityId,
                    Name = d.Name,
                    LongName = $"{d.PackageName}.{d.Name}",
                    FilePath = d.FilePath,
                    Contents = d.Content,
                    Package = knownPackageEntities.First(p => p.LongName == d.PackageName),
                    ParentId = fileEntities.First(p => p.FilePath == d.FilePath).Id,
                    Kind = EntityKindUtils.GetAnnotationTypeKind(d.Name, d.Modifier),
                    Line = d.Line,
                    Column = d.Column
                })
                .ToList();

        var unknownEntities =
            JavaTypeDeclarations
                .Where(d => d.Kind == JavaTypeDeclarationKind.FromImport)
                .Where(d => knownPackageEntities.All(p => p.LongName != d.PackageName))
                .GroupBy(d => $"{d.PackageName}.{d.Name}")
                .Select(g => g.First())
                .GroupBy(d => d.PackageName)
                .SelectMany(g =>
                {
                    var package = new JavaEntity
                    {
                        Id = NewEntityId,
                        Name = g.Key.Split('.')[^1],
                        LongName = g.Key,
                        FilePath = g.First().FilePath,
                        Contents = "",
                        Package = null,
                        ParentId = null,
                        Kind = "Java Unknown Package",
                        Line = g.First().Line,
                        Column = g.First().Column
                    };

                    var unknownClasses =
                        g.Select(d => new JavaEntity
                        {
                            Id = NewEntityId,
                            Name = d.Name,
                            LongName = $"{d.PackageName}.{d.Name}",
                            FilePath = d.FilePath,
                            Contents = "",
                            Package = package,
                            ParentId = null,
                            Kind = "Java Unknown Class Type Member",
                            Line = d.Line,
                            Column = d.Column
                        });

                    return new[] {package}.Concat(unknownClasses);
                })
                .ToList();

        var entities =
            fileEntities
                .Concat(knownPackageEntities)
                .Concat(classEntities)
                .Concat(interfaceEntities)
                .Concat(enumEntities)
                .Concat(interfaceAnnotationEntities)
                .Concat(unknownEntities)
                .ToList();

        JavaEntities.AddRange(entities);
        return JavaEntities;
    }

    public IEnumerable<JavaReference> ExtractReferences(string[] refs)
    {
        JavaReferences.Clear();

        var containReferences = ExtractContainReferences();
        var containInReferences = ExtractContainInReferences(containReferences);
        var extendCoupleReferences = ExtractExtendCoupleReferences();
        var extendByCoupleByReferences = ExtractExtendByCoupleByReferences(extendCoupleReferences);

        if (refs.Contains(JavaReferenceKinds.Contain, StringComparer.InvariantCultureIgnoreCase))
            JavaReferences.AddRange(containReferences);

        if (refs.Contains(JavaReferenceKinds.ContainIn, StringComparer.InvariantCultureIgnoreCase))
            JavaReferences.AddRange(containInReferences);

        if (refs.Contains(JavaReferenceKinds.Extend, StringComparer.InvariantCultureIgnoreCase))
            JavaReferences.AddRange(extendCoupleReferences);

        if (refs.Contains(JavaReferenceKinds.ExtendBy, StringComparer.InvariantCultureIgnoreCase))
            JavaReferences.AddRange(extendByCoupleByReferences);

        return JavaReferences;
    }

    private List<JavaReference> ExtractExtendByCoupleByReferences(List<JavaReference> extendCoupleReferences)
    {
        return extendCoupleReferences
            .Select(r => new JavaReference
            {
                Id = NewReferenceId,
                EntId = r.ScopeId,
                ScopeId = r.EntId,
                Line = r.Line,
                Column = r.Column,
                FileId = r.FileId,
                Kind = JavaReferenceKinds.ExtendBy
            })
            .ToList();
    }

    private List<JavaReference> ExtractExtendCoupleReferences()
    {
        return JavaTypeDeclarations
            .Where(d => d.Extends is not null)
            .SelectMany(d => Enumerable.Repeat(d, d.Extends!.Length).Zip(d.Extends))
            .Select(it =>
            {
                var (typeDec, ext) = it;

                var matchInPackage =
                    JavaTypeDeclarations
                        .Where(it2 => it2.PackageName.Equals(typeDec.PackageName))
                        .Where(it2 =>
                            it2.Kind is JavaTypeDeclarationKind.Class or JavaTypeDeclarationKind.Interface)
                        .FirstOrDefault(it2 => $"{it2.PackageName}.{it2.Name}".EndsWith(ext));

                if (matchInPackage is not null)
                {
                    return (First: typeDec, matchInPackage);
                }

                var matchInImports =
                    JavaTypeDeclarations
                        .Where(it2 => it2.FilePath == typeDec.FilePath)
                        .Where(it2 => it2.Kind is JavaTypeDeclarationKind.FromImport)
                        .FirstOrDefault(it2 => $"{it2.PackageName}.{it2.Name}".EndsWith(ext));

                return matchInImports is not null ? (First: typeDec, matchInImports) : (null, null);
            })
            .Where(it => it.Item2 is not null)
            .Select(it =>
            {
                var selfEntity = JavaEntities
                    .FirstOrDefault(e =>
                        e.LongName == $"{it.First!.PackageName}.{it.First.Name}"
                    );

                var otherEntity = JavaEntities
                    .FirstOrDefault(e =>
                        e.LongName == $"{it.Item2!.PackageName}.{it.Item2!.Name}"
                    );

                return (selfEntity, otherEntity);
            })
            .Where(it => it.selfEntity is not null && it.otherEntity is not null)
            .Select(it => new JavaReference
            {
                Id = NewReferenceId,
                EntId = it.otherEntity!.Id,
                ScopeId = it.selfEntity!.Id,
                Line = it.selfEntity!.Line!.Value,
                Column = it.selfEntity!.Column!.Value,
                FileId = JavaEntities.First(je => je.Kind == "Java File" && je.FilePath == it.selfEntity!.FilePath)
                    .Id,
                Kind = JavaReferenceKinds.Extend
            })
            .ToList();
    }

    private List<JavaReference> ExtractContainInReferences(List<JavaReference> containReferences)
    {
        return containReferences
            .Select(cf => new JavaReference
            {
                Id = NewReferenceId,
                EntId = cf.ScopeId,
                ScopeId = cf.EntId,
                Line = cf.Line,
                Column = cf.Column,
                FileId = cf.FileId,
                Kind = JavaReferenceKinds.ContainIn
            })
            .ToList();
    }

    private List<JavaReference> ExtractContainReferences()
    {
        return JavaEntities
            .Where(e =>
                e.Kind != "Java File"
                && e.Kind != "Java Package"
                && e.Kind != "Java Unknown Package")
            .Select(e => new JavaReference
            {
                Id = NewReferenceId,
                EntId = e.Id,
                ScopeId = e.Package!.Id,
                Line = e.Line!.Value,
                Column = e.Column!.Value,
                FileId = JavaEntities.First(je => je.Kind == "Java File" && je.FilePath == e.FilePath).Id,
                Kind = JavaReferenceKinds.Contain
            })
            .ToList();
    }
}