package pl.dr.forum;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.ArrayList;
import java.util.List;

@Slf4j
@Controller
@RequestMapping("/topic")
public class TopicController {

    private List<String> comments;

    @GetMapping
    public String topic(Model model){
        String topic = "O testowaniu aplikacji";
        comments = new ArrayList<>();
        comments.add("O ptakach");
        comments.add("O drzewach");

        model.addAttribute("topic", topic);
        model.addAttribute("comments", comments);
        return "topic";
    }

    @PutMapping("/topic/comment")
    public String addComment(Model model){
        String topic = "O testowaniu aplikacji";
        List<String> comments = new ArrayList<>();
        comments.add("O ptakach");
        comments.add("O drzewach");

        model.addAttribute("newComment", new String());
        model.addAttribute("topic", topic);
        model.addAttribute("comments", comments);
        return "topic";
    }

}
