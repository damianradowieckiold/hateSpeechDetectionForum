package pl.dr.forum;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import pl.dr.forum.model.Comment;
import pl.dr.forum.model.Topic;
import pl.dr.forum.repository.CommentRepository;
import pl.dr.forum.repository.TopicRepository;
import pl.dr.forum.service.HateSpeechService;

import javax.validation.Valid;
import javax.validation.constraints.Size;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Slf4j
@Controller
@RequestMapping("/topic")
public class TopicController {

    @Autowired
    private TopicRepository topicRepository;

    @Autowired
    private CommentRepository commentRepository;

    @Autowired
    private HateSpeechService hateSpeechService;

    @GetMapping("/{id}")
    public String topic(@PathVariable("id") int topicId, Model model){
        Optional<Topic> topic = topicRepository.findById(topicId);
        model.addAttribute("topic", topic.orElse(new Topic()));
        model.addAttribute("comments", topic.isPresent() ? filter(topic.get().getComments()) : Collections.emptyList());
        model.addAttribute("newComment", new Comment());
        return "topic";
    }

    @PostMapping("/{id}/comment")
    public String addComment(@PathVariable("id") int topicId, @Valid Comment newComment, BindingResult bindingResult, Model model) throws NoSuchFieldException {
        Topic topic = topicRepository.findById(topicId).orElseThrow(IllegalStateException::new);

        if(!bindingResult.hasErrors()){
            //TODO hate speech validation
            topic.addComment(newComment);
            newComment.setTopic(topic);
            commentRepository.save(newComment);
            topicRepository.save(topic);
        }
        else{
            model.addAttribute("error",  newComment.getClass().getDeclaredField("content").getDeclaredAnnotation(Size.class).message());
        }

        model.addAttribute("topic", topic);
        model.addAttribute("comments", filter(topic.getComments()));
        model.addAttribute("newComment", new Comment());
        return "topic";
    }

    @PostMapping("/{id}/comment/{commentId}")
    public String markCommentAsHateSpeech(@PathVariable("id") int topicId, @PathVariable("commentId") int commentId, Model model){
        Comment comment = commentRepository.findById(commentId).orElseThrow(IllegalArgumentException::new);
        comment.setHateSpeechCount(comment.getHateSpeechCount() + 1);
        commentRepository.save(comment);
        String info ="";
        if(comment.getHateSpeechCount() >= Comment.HATE_SPEECH_COUNTER_LIMIT){
            hateSpeechService.markAsHateSpeech(comment);
            info = "Komentarz zakwalifikowany jako hate speech";
        }
        Topic topic = topicRepository.findById(topicId).orElseThrow(IllegalStateException::new);
        model.addAttribute("topic", topic);
        model.addAttribute("comments", filter(topic.getComments()));
        model.addAttribute("newComment", new Comment());
        model.addAttribute("info", info);
        return "topic";
    }

    private List<Comment> filter(List<Comment> comments){
        return comments
                .stream()
                .filter(c -> !c.isHateSpeech())
                .collect(Collectors.toList());
    }

}
