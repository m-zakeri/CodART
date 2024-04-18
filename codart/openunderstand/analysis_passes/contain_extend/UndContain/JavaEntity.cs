namespace UndContain;

public class JavaEntity
{
    public int Id { get; set; }
    public int? ParentId { get; set; }
    public JavaEntity? Package { get; set; }
    public string Kind { get; set; }
    public int? KindId { get; set; }
    public string Name { get; set; }
    public string LongName { get; set; }
    public string? Contents { get; set; }
    public string FilePath { get; set; }
    public int? Line { get; set; }
    public int? Column { get; set; }
}