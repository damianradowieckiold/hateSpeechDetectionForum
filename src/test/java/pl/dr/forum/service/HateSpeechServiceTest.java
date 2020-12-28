package pl.dr.forum.service;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import pl.dr.forum.ForumApplication;

import static org.junit.jupiter.api.Assertions.assertTrue;

@ExtendWith(SpringExtension.class)
@ContextConfiguration(classes = { ForumApplication.class })
class HateSpeechServiceTest {

    @Autowired
    private HateSpeechService hateSpeechService;

    @Test
    void isHateSpeech() {
        assertTrue(hateSpeechService.isHateSpeech("kurwa"));
    }
}