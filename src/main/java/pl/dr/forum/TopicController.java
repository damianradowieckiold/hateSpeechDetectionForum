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
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;
import java.util.stream.Collectors;

@Slf4j
@Controller
@RequestMapping("/topic")
public class TopicController {

    public static final String NEW_COMMENT_IS_HATE_SPEECH = "Nowy komentarz jest obraźliwy, nie może zostać dodany.";
    public static final String COMMENT_QUALIFIED_AS_HATE_SPEECH = "Komentarz zakwalifikowany jako hate speech";
    @Autowired
    private TopicRepository topicRepository;

    @Autowired
    private CommentRepository commentRepository;

    @Autowired
    private HateSpeechService hateSpeechService;

    @GetMapping("/{id}")
    public String topic(@PathVariable("id") int topicId, Model model){
        Topic topic = topicRepository.findById(topicId).orElseThrow(IllegalStateException::new);
        return toTopicPage(model, topic);
    }

    @PostMapping("/{id}/comment")
    public String addComment(@PathVariable("id") int topicId, @Valid Comment newComment, BindingResult bindingResult, Model model) throws NoSuchFieldException {
        Topic topic = topicRepository.findById(topicId).orElseThrow(IllegalStateException::new);

        if(bindingResult.hasErrors()){
            model.addAttribute("error", retrieveAnnotationMessage(newComment));
        } else if(hateSpeechService.isHateSpeech(newComment.getContent())){
            model.addAttribute("error", NEW_COMMENT_IS_HATE_SPEECH);
        } else{
            addComment(newComment, topic);
        }

        return toTopicPage(model, topic);
    }

    private String retrieveAnnotationMessage(@Valid Comment newComment) throws NoSuchFieldException {
        return newComment.getClass().getDeclaredField("content").getDeclaredAnnotation(Size.class).message();
    }

    @PostMapping("/{id}/comment/{commentId}")
    public String markCommentAsHateSpeech(@PathVariable("id") int topicId, @PathVariable("commentId") int commentId, Model model){
        Comment comment = markAsPotentialHateSpeech(commentId);
        String info = "";
        if(comment.isHateSpeech()){
            info = COMMENT_QUALIFIED_AS_HATE_SPEECH;
        }
        Topic topic = topicRepository.findById(topicId).orElseThrow(IllegalStateException::new);
        model.addAttribute("info", info);
        return toTopicPage(model, topic);
    }

    /**
     * Marks comment as potential hate speech. If comment will reach Comment.HATE_SPEECH_COUNTER_LIMIT,
     * then comment is marked as hate speech.
     */
    private Comment markAsPotentialHateSpeech(int commentId){
        Comment comment = commentRepository.findById(commentId).orElseThrow(IllegalArgumentException::new);
        comment.setHateSpeechCount(comment.getHateSpeechCount() + 1);
        if(comment.getHateSpeechCount() >= Comment.HATE_SPEECH_COUNTER_LIMIT){
            hateSpeechService.markAsHateSpeech(comment);
            addToHateSpeechCommentsList(comment.getContent());
        }
        commentRepository.save(comment);
        return comment;
    }

    private void addToHateSpeechCommentsList(String comment) {
        String result = comment + ",hateful";
        try (FileWriter pw = new FileWriter("src/main/resources/forum_comments/hate_speech.csv",true)){
            pw.append(result);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private String toTopicPage(Model model, Topic topic) {
        model.addAttribute("topic", topic);
        model.addAttribute("comments", filter(topic.getComments()));
        model.addAttribute("newComment", new Comment());
        return "topic";
    }

    private List<Comment> filter(List<Comment> comments){
        return comments
                .stream()
                .filter(c -> !c.isHateSpeech())
                .collect(Collectors.toList());
    }

    private void addComment(@Valid Comment newComment, Topic topic) {
        topic.addComment(newComment);
        newComment.setTopic(topic);
        commentRepository.save(newComment);
        topicRepository.save(topic);
    }

    public static void main(String[] args) {
        TopicController topicController = new TopicController();
        topicController.addToHateSpeechCommentsList("Spalić wszystkich żydów");
    }

}
