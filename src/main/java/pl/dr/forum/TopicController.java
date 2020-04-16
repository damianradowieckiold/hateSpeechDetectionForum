package pl.dr.forum;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import pl.dr.forum.model.Comment;
import pl.dr.forum.model.Topic;
import pl.dr.forum.repository.CommentRepository;
import pl.dr.forum.repository.TopicRepository;

import java.util.Collections;
import java.util.Optional;

@Slf4j
@Controller
@RequestMapping("/topic")
public class TopicController {

    @Autowired
    private TopicRepository topicRepository;

    @Autowired
    private CommentRepository commentRepository;

    @GetMapping("/{id}")
    public String topic(@PathVariable("id") int topicId, Model model){
        Optional<Topic> topic = topicRepository.findById(topicId);
        model.addAttribute("topic", topic.orElse(new Topic()));
        model.addAttribute("comments", topic.isPresent() ? topic.get().getComments() : Collections.emptyList());
        model.addAttribute("newComment", new Comment());
        return "topic";
    }

    @PostMapping("/{id}/comment")
    public String addComment(@PathVariable("id") int topicId, Comment newComment, Model model){
        Topic topic = topicRepository.findById(topicId).orElseThrow(IllegalStateException::new);
        topic.addComment(newComment);
        newComment.setTopic(topic);
        commentRepository.save(newComment);
        topicRepository.save(topic);
        model.addAttribute("topic", topic);
        model.addAttribute("comments", topic.getComments());
        model.addAttribute("newComment", new Comment());
        return "topic";
    }

}
