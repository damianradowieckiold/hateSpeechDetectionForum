package pl.dr.forum;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import pl.dr.forum.service.HateSpeechService;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

import static org.junit.jupiter.api.Assertions.assertTrue;

@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = { ForumApplication.class })
public class OverallTest {

    @Autowired
    private HateSpeechService hateSpeechService;

    @Test
    void obrazliwe() throws FileNotFoundException {
        File obrazliwe = new File("src/main/resources/polish_comments/obrazliwe.csv");
        Scanner scanner = new Scanner(obrazliwe);

        int hate_speech_count = 0;
        int normal_count = 0;

        while(scanner.hasNextLine()){
            System.out.println("-----------------------");
            System.out.println("all_count:" + (hate_speech_count + normal_count));
            System.out.println("hate_speech_count: " + hate_speech_count);
            System.out.println("normal_count: " + normal_count);
            System.out.println("-----------------------");
            if (hateSpeechService.isHateSpeech(scanner.nextLine())) {
                hate_speech_count++;
            } else {
                normal_count++;
            }
        }


        assertTrue(hate_speech_count > normal_count);
    }

    @Test
    void grozby_karalne() throws FileNotFoundException {
        File grozby_karalne = new File("src/main/resources/polish_comments/grozby_karalne.csv");
        Scanner scanner = new Scanner(grozby_karalne);

        int hate_speech_count = 0;
        int normal_count = 0;

        while(scanner.hasNextLine()){
            System.out.println("-----------------------");
            System.out.println("all_count:" + (hate_speech_count + normal_count));
            System.out.println("hate_speech_count: " + hate_speech_count);
            System.out.println("normal_count: " + normal_count);
            System.out.println("-----------------------");
            if (hateSpeechService.isHateSpeech(scanner.nextLine())) {
                hate_speech_count++;
            } else {
                normal_count++;
            }
        }


        assertTrue(hate_speech_count > normal_count);
    }

}
