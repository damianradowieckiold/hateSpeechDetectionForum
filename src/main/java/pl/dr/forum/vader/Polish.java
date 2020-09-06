package pl.dr.forum.vader;

import net.nunoachenriques.vader.lexicon.English;
import net.nunoachenriques.vader.lexicon.Language;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Polish implements Language {
    private static final ClassLoader LOADER = English.class.getClassLoader();
    private static final List<String> PUNCTUATION = Arrays.asList(".", "!", "?", ",", ";", ":", "-", "'", "\"", "!!", "!!!", "??", "???", "?!?", "!?!", "?!?!", "!?!?");
    private static final List<String> NEGATIVE_WORDS = Arrays.asList("nie", "brak", "", //TODO
            "cant", "couldnt", "darent", "didnt", "doesnt", "ain't", "aren't", "can't", "couldn't",
            "daren't", "didn't", "doesn't", "dont", "hadnt", "hasnt", "havent", "isnt", "mightnt",
            "mustnt", "neither", "don't", "hadn't", "hasn't", "haven't", "isn't", "mightn't", "mustn't",
            "neednt", "needn't", "never", "none", "nope", "nor", "not", "nothing", "nowhere", "oughtnt",
            "shant", "shouldnt", "uhuh", "wasnt", "werent", "oughtn't", "shan't", "shouldn't", "uh-uh",
            "wasn't", "weren't", "without", "wont", "wouldnt", "won't", "wouldn't", "rarely", "seldom", "despite");
    private static final Map<String, Float> BOOSTER_DICTIONARY = createBoosterDictionary();
    private static final Map<String, Float> SENTIMENT_LADEN_IDIOMS = createSentimentLadenIdioms();
    private static final Map<String, Float> WORD_VALENCE_DICTIONARY = getWordValenceDictionary("net/nunoachenriques/vader/lexicon/english.txt");

    private static Map<String, Float> createBoosterDictionary() {
        Map<String, Float> m = new HashMap();
        m.put("decidedly", 0.293F);
        m.put("uber", 0.293F);
        m.put("barely", -0.293F);
        m.put("particularly", 0.293F);
        m.put("enormously", 0.293F);
        m.put("less", -0.293F);
        m.put("absolutely", 0.293F);
        m.put("kinda", -0.293F);
        m.put("flipping", 0.293F);
        m.put("awfully", 0.293F);
        m.put("purely", 0.293F);
        m.put("majorly", 0.293F);
        m.put("substantially", 0.293F);
        m.put("partly", -0.293F);
        m.put("remarkably", 0.293F);
        m.put("really", 0.293F);
        m.put("sort of", -0.293F);
        m.put("little", -0.293F);
        m.put("fricking", 0.293F);
        m.put("sorta", -0.293F);
        m.put("amazingly", 0.293F);
        m.put("kind of", -0.293F);
        m.put("just enough", -0.293F);
        m.put("fucking", 0.293F);
        m.put("occasionally", -0.293F);
        m.put("somewhat", -0.293F);
        m.put("kindof", -0.293F);
        m.put("friggin", 0.293F);
        m.put("incredibly", 0.293F);
        m.put("totally", 0.293F);
        m.put("marginally", -0.293F);
        m.put("more", 0.293F);
        m.put("considerably", 0.293F);
        m.put("fabulously", 0.293F);
        m.put("hardly", -0.293F);
        m.put("very", 0.293F);
        m.put("sortof", -0.293F);
        m.put("kind-of", -0.293F);
        m.put("scarcely", -0.293F);
        m.put("thoroughly", 0.293F);
        m.put("quite", 0.293F);
        m.put("most", 0.293F);
        m.put("completely", 0.293F);
        m.put("frigging", 0.293F);
        m.put("intensely", 0.293F);
        m.put("utterly", 0.293F);
        m.put("highly", 0.293F);
        m.put("extremely", 0.293F);
        m.put("unbelievably", 0.293F);
        m.put("almost", -0.293F);
        m.put("especially", 0.293F);
        m.put("fully", 0.293F);
        m.put("frickin", 0.293F);
        m.put("tremendously", 0.293F);
        m.put("exceptionally", 0.293F);
        m.put("flippin", 0.293F);
        m.put("hella", 0.293F);
        m.put("so", 0.293F);
        m.put("greatly", 0.293F);
        m.put("hugely", 0.293F);
        m.put("deeply", 0.293F);
        m.put("unusually", 0.293F);
        m.put("entirely", 0.293F);
        m.put("slightly", -0.293F);
        m.put("effing", 0.293F);
        return m;
    }

    private static Map<String, Float> createSentimentLadenIdioms() {
        Map<String, Float> m = new HashMap();
        m.put("cut the mustard", 2.0F);
        m.put("bad ass", 1.5F);
        m.put("kiss of death", -1.5F);
        m.put("yeah right", -2.0F);
        m.put("the bomb", 3.0F);
        m.put("hand to mouth", -2.0F);
        m.put("the shit", 3.0F);
        return m;
    }

    private static Map<String, Float> getWordValenceDictionary(String filename) {
        InputStream lexFile = LOADER.getResourceAsStream(filename);
        Map<String, Float> lexDictionary = new HashMap();
        if (lexFile != null) {
            try {
                BufferedReader br = new BufferedReader(new InputStreamReader(lexFile));

                String line;
                try {
                    while ((line = br.readLine()) != null) {
                        String[] lexFileData = line.split("\\t");
                        String currentText = lexFileData[0];
                        Float currentTextValence = Float.parseFloat(lexFileData[1]);
                        lexDictionary.put(currentText, currentTextValence);
                    }
                } catch (Throwable var9) {
                    try {
                        br.close();
                    } catch (Throwable var8) {
                        var9.addSuppressed(var8);
                    }

                    throw var9;
                }

                br.close();
            } catch (IOException var10) {
                //TODO Logger.error(var10);
            }
        }

        return lexDictionary;
    }

    public Polish() {
    }

    public List<String> getPunctuation() {
        return PUNCTUATION;
    }

    public List<String> getNegativeWords() {
        return NEGATIVE_WORDS;
    }

    public Map<String, Float> getBoosterDictionary() {
        return BOOSTER_DICTIONARY;
    }

    public Map<String, Float> getSentimentLadenIdioms() {
        return SENTIMENT_LADEN_IDIOMS;
    }

    public Map<String, Float> getWordValenceDictionary() {
        return WORD_VALENCE_DICTIONARY;
    }

    public boolean isUpper(String token) {
        if (token.toLowerCase().startsWith("http://")) {
            return false;
        } else if (!token.matches(".*[a-zA-Z]+.*")) {
            return false;
        } else {
            for (int i = 0; i < token.length(); ++i) {
                if (Character.isLowerCase(token.charAt(i))) {
                    return false;
                }
            }

            return true;
        }
    }
}
