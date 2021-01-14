package pl.dr.forum.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import pl.dr.forum.model.Comment;
import pl.dr.forum.repository.CommentRepository;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@Service
@Slf4j
public class HateSpeechService {

    @Autowired
    private CommentRepository commentRepository;

    public void markAsHateSpeech(Comment comment){
        comment.setHateSpeech(true);
        commentRepository.save(comment);
    }

    public boolean isHateSpeech(String text){
        return askPython(Path.of("src/main/python/predictor.py"), text);
    }

    private boolean askPython(Path scriptPath, String comment){
        log.debug("calling script:" + scriptPath);
        try {
            List<String> process_args = new ArrayList<>(Arrays.asList("python", scriptPath.toAbsolutePath().toString(), comment));
            ProcessBuilder pb = new ProcessBuilder(process_args);
            pb.redirectErrorStream(true);

            Process proc = pb.start();

            String output = "False";
            String line;
            BufferedReader in = new BufferedReader(new InputStreamReader(
                    proc.getInputStream()));
            while ((line = in.readLine()) != null) {
                log.debug(line);
                output = line;
            }

            proc.destroy();
            log.debug("Python code returned:" + output);
            return Boolean.parseBoolean(output);
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }
    }

    public static void main(String[] args) {
        HateSpeechService service = new HateSpeechService();
        boolean result = service.isHateSpeech("Będziesz brzmiał tak cholernie głupio i nieświadomie co do tej suki !!");
        System.out.println(result);
    }

}
