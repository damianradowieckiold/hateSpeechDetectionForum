package pl.dr.forum;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import pl.dr.forum.model.Topic;
import pl.dr.forum.repository.TopicRepository;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

@Slf4j
@Controller
@RequestMapping("/topic")
public class TopicController {

    @Autowired
    private TopicRepository topicRepository;

    @GetMapping("/{id}")
    public String topic(@PathVariable("id") int topicId, Model model){
        Optional<Topic> topic = topicRepository.findById(topicId);
        model.addAttribute("topic", topic.orElse(new Topic()));
        model.addAttribute("comments", topic.isPresent() ? topic.get().getComments() : Collections.emptyList());
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
