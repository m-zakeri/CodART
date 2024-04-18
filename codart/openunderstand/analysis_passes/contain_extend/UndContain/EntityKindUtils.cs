using System;
using System.Text.RegularExpressions;

namespace UndContain;

public static class EntityKindUtils
{
    public static string GetClassKind(string name, string modifier)
    {
        // Java Static Final Abstract Generic Class Type [Public, Protected, Private, Default] Member
        var visibility = "Default";
        foreach (var v in new[] {"Public", "Protected", "Private"})
            if (modifier.StartsWith(v, StringComparison.InvariantCultureIgnoreCase))
                visibility = v;

        var isGeneric = Regex.IsMatch(name, @"<.+>$");
        var isStatic = modifier.Contains("Static", StringComparison.InvariantCultureIgnoreCase);
        var isFinal = modifier.Contains("Final", StringComparison.InvariantCultureIgnoreCase);
        var isAbstract = modifier.Contains("Abstract", StringComparison.InvariantCultureIgnoreCase);

        var kind = "Java ";
        kind += isStatic ? "Static " : "";
        kind += isFinal ? "Final " : "";
        kind += isAbstract ? "Abstract " : "";
        kind += isGeneric ? "Generic " : "";
        kind += $"Class Type {visibility} Member";

        return kind;
    }

    public static string GetInterfaceKind(string name, string modifier)
    {
        // Java Generic Interface Type [Public, Protected, Private, Default]
        var visibility = "Default";
        foreach (var v in new[] {"Public", "Protected", "Private"})
            if (modifier.StartsWith(v, StringComparison.InvariantCultureIgnoreCase))
                visibility = v;

        var isGeneric = Regex.IsMatch(name, @"<.+>$");

        var kind = "Java ";
        kind += isGeneric ? "Generic " : "";
        kind += $"Interface Type {visibility}";

        return kind;
    }

    public static string GetEnumKind(string name, string modifier)
    {
        // Java Enum Class Type [Public, Protected, Private, Default] Member
        var visibility = "Default";
        foreach (var v in new[] {"Public", "Protected", "Private"})
            if (modifier.StartsWith(v, StringComparison.InvariantCultureIgnoreCase))
                visibility = v;

        var kind = "Java ";
        kind += $"Enum Class Type {visibility} Member";

        return kind;
    }

    public static string GetAnnotationTypeKind(string name, string modifier)
    {
        // Java Annotation Interface Type [Public, Protected, Private, Default]
        var visibility = "Default";
        foreach (var v in new[] {"Public", "Protected", "Private"})
            if (modifier.StartsWith(v, StringComparison.InvariantCultureIgnoreCase))
                visibility = v;

        var kind = "Java ";
        kind += $"Interface Type {visibility}";

        return kind;
    }
}