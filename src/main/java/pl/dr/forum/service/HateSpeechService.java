package pl.dr.forum.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import pl.dr.forum.model.Comment;
import pl.dr.forum.repository.CommentRepository;

@Service
public class HateSpeechService {

    @Autowired
    private CommentRepository commentRepository;

    public void markAsHateSpeech(Comment comment){
        comment.setHateSpeech(true);
        commentRepository.save(comment);
    }
}
