package pl.dr.forum.vader;

import net.nunoachenriques.vader.text.Tokenizer;

import java.util.Arrays;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.regex.Pattern;

public class PolishTokenizer implements Tokenizer {
    private static final Pattern WHITESPACE_PATTERN = Pattern.compile("\\p{Space}");
    private static final Pattern PUNCTUATION_EXCLUDE_CONTRACTION_PATTERN = Pattern.compile("[\\p{Punct}&&[^.']]|(?<=(^|\\s|\\p{Punct}))[.']|[.'](?=($|\\s|\\p{Punct}))");

    public PolishTokenizer() {
    }

    public List<String> split(String s, Pattern p) {
        return new LinkedList(Arrays.asList(p.split(s)));
    }

    public List<String> cleanAndSplit(String s, Pattern p, Pattern c, String r) {
        return new LinkedList(Arrays.asList(p.split(c.matcher(s).replaceAll(r))));
    }

    public List<String> splitWhitespace(String s) {
        return this.split(s, WHITESPACE_PATTERN);
    }

    public List<String> cleanPunctuationAndSplitWhitespace(String s, String r) {
        return this.cleanAndSplit(s, WHITESPACE_PATTERN, PUNCTUATION_EXCLUDE_CONTRACTION_PATTERN, r);
    }

    public void removeTokensBySize(List<String> l, int min, int max) {
        Iterator i = l.iterator();

        while(true) {
            String t;
            do {
                if (!i.hasNext()) {
                    return;
                }

                t = (String)i.next();
            } while(t.length() >= min && t.length() <= max);

            i.remove();
        }
    }
}
