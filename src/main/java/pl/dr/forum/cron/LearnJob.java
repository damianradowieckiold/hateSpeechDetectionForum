package pl.dr.forum.cron;

import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@Component
@Slf4j
public class LearnJob {

    @Scheduled(cron = "0 0 0 * * *")
    public void learn() {
        try {
            Path path = Path.of("src/main/python/learning.py");
            List<String> process_args = new ArrayList<>(Arrays.asList("python", path.toAbsolutePath().toString()));
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
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


}
