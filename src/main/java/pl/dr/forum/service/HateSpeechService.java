package pl.dr.forum.service;

import net.nunoachenriques.vader.SentimentAnalysis;
import opennlp.tools.doccat.*;
import opennlp.tools.langdetect.*;
import opennlp.tools.ml.perceptron.PerceptronTrainer;
import opennlp.tools.sentdetect.SentenceDetectorME;
import opennlp.tools.sentdetect.SentenceModel;
import opennlp.tools.util.*;
import opennlp.tools.util.model.ModelUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import pl.dr.forum.model.Comment;
import pl.dr.forum.repository.CommentRepository;
import pl.dr.forum.vader.Polish;
import pl.dr.forum.vader.PolishTokenizer;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Map;
import java.util.Scanner;

@Service
public class HateSpeechService {

    private static final float TRESHOLD = .7f;

    @Autowired
    private CommentRepository commentRepository;

    public void markAsHateSpeech(Comment comment){
        comment.setHateSpeech(true);
        commentRepository.save(comment);
    }

    public boolean isHateSpeech(Comment comment){
        return comment.getContent().toLowerCase().equals("kurwa") || comment.getContent().toLowerCase().equals("fuck");
    }

    public static void main(String[] args) throws IOException {
        ArrayList<String> sentences = new ArrayList<String>() {{
            add("VADER is smart, handsome, and funny.");
            add("VADER is smart, handsome, and funny!");
            add("VADER is very smart, handsome, and funny.");
            add("VADER is VERY SMART, handsome, and FUNNY.");
            add("VADER is VERY SMART, handsome, and FUNNY!!!");
            add("VADER is VERY SMART, really handsome, and INCREDIBLY FUNNY!!!");
            add("The book was good.");
            add("The book was kind of good.");
            add("The plot was good, but the characters are uncompelling and the dialog is not great.");
            add("A really bad, horrible book.");
            add("At least it isn't a horrible book.");
            add(":) and :D");
            add("");
            add("Today sux");
            add("Today sux!");
            add("Today SUX!");
            add("Today kinda sux! But I'll get by, lol");
            add("Fuck you");
            add("Thank you");
        }};

        for (String sentence : sentences) {
            System.out.println(sentence);
            SentimentAnalysis sentimentAnalysis = new SentimentAnalysis(new Polish(), new PolishTokenizer());
            Map<String, Float> result = sentimentAnalysis.getSentimentAnalysis(sentence);
            //System.out.println(sentimentAnalyzer.getPolarity());
            for(String key: result.keySet()){
                System.out.println(key + " : " + result.get(key));
            }
        }
    }

    public static void main1(String [] args) throws IOException {

        /*String sentence = "Hi. How are you? Welcome to Tutorialspoint. "
                + "We provide free tutorials on various technologies";*/

        String sentence = "Cześć, Jak się masz? Witaj u nas. Dostarczamy tutoriale dla wielu technologii";

        InputStream inputStream = new FileInputStream("F:\\WSEI\\Studia\\praca_magisterska\\projekt\\forum\\src\\main\\resources\\models\\en-sent.bin");
        SentenceModel model = new SentenceModel(inputStream);
        SentenceDetectorME detector = new SentenceDetectorME(model);
        String sentences[] = detector.sentDetect(sentence);

        for(String sent : sentences)
            System.out.println(sent);
    }

    public static void main2(String[] args) throws IOException {
        InputStreamFactory inputStreamFactory = new MarkableFileInputStreamFactory(new File("corpus.txt"));

        ObjectStream<String> lineStream =
                new PlainTextByLineStream(inputStreamFactory, StandardCharsets.UTF_8);
        ObjectStream<LanguageSample> sampleStream = new LanguageDetectorSampleStream(lineStream);

        TrainingParameters params = ModelUtil.createDefaultTrainingParameters();
        params.put(TrainingParameters.ALGORITHM_PARAM,
                PerceptronTrainer.PERCEPTRON_VALUE);
        params.put(TrainingParameters.CUTOFF_PARAM, 0);

        LanguageDetectorFactory factory = new LanguageDetectorFactory();

        LanguageDetectorModel model = LanguageDetectorME.train(sampleStream, params, factory);
        model.serialize(new File("langdetect.bin"));
    }

    public static void predictLanguage(String[] args) throws IOException {
        //reading created model
        InputStream is = new FileInputStream("");
        LanguageDetectorModel model = new LanguageDetectorModel(is);

        //creating detector
        LanguageDetector detector = new LanguageDetectorME(model);

        //predicting
        Language bestLanguage = detector.predictLanguage("Jaki to język?");
        System.out.println("Best language: " + bestLanguage.getLang());
        System.out.println("Best language confidence: " + bestLanguage.getConfidence());

    }

    public static void trainLanguageDetector(String[] args) throws IOException {
        //reading samples
        InputStreamFactory inputStreamFactory = new MarkableFileInputStreamFactory(new File("C:\\Users\\Damian\\IdeaProjects\\forum\\src\\main\\resources\\training_data"));
        ObjectStream<String> lineStream = new PlainTextByLineStream(inputStreamFactory, StandardCharsets.UTF_8);
        ObjectStream<DocumentSample> sampleStream = new DocumentSampleStream(lineStream);

        //params
        TrainingParameters params = ModelUtil.createDefaultTrainingParameters();
        params.put(TrainingParameters.CUTOFF_PARAM, 0);
        DoccatFactory factory = new DoccatFactory(new FeatureGenerator[] { new BagOfWordsFeatureGenerator() });
        DoccatModel model = DocumentCategorizerME.train("pol", sampleStream, params, factory);
        model.serialize(new File("documentcategorizer.bin"));

        try (InputStream modelIn = new FileInputStream("documentcategorizer.bin");
             Scanner scanner = new Scanner(System.in);) {

            while (true) {
                // Get inputs in loop
                System.out.println("Enter a sentence:");

                // Initialize document categorizer tool
                DocumentCategorizerME myCategorizer = new DocumentCategorizerME(model);

                // Get the probabilities of all outcome i.e. positive & negative
                double[] probabilitiesOfOutcomes = myCategorizer.categorize(getTokens(scanner.nextLine()));

                // Get name of category which had high probability
                String category = myCategorizer.getBestCategory(probabilitiesOfOutcomes);
                System.out.println("Category: " + category);

            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static String[] getTokens(String sentence) {
        return sentence.split(" ");
    }

    public static void categorize(String[] args) throws IOException {
        InputStream is = new FileInputStream("C:\\Users\\Damian\\IdeaProjects\\forum\\src\\main\\resources\\training_data");
        DoccatModel m = new DoccatModel(is);

        String inputText [] = new String[]{"Tak"};
        DocumentCategorizerME categorizer = new DocumentCategorizerME(m);
        double[] outcomes = categorizer.categorize(inputText);
        String category = categorizer.getBestCategory(outcomes);
    }

    public static void main3(String[] args) throws IOException {
        trainLanguageDetector(args);
    }

}
