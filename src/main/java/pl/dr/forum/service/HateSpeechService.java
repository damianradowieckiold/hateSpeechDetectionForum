package pl.dr.forum.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import pl.dr.forum.model.Comment;
import pl.dr.forum.repository.CommentRepository;

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


}
