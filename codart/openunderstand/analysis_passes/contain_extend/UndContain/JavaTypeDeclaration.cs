namespace UndContain;

public class JavaTypeDeclaration
{
    public JavaTypeDeclarationKind Kind { get; set; }
    public string PackageName { get; set; }
    public string Modifier { get; set; }
    public string Name { get; set; }
    public string Content { get; set; }
    public int Line { get; set; }
    public int Column { get; set; }
    public string FilePath { get; set; }
    public string[]? Extends { get; set; }
}