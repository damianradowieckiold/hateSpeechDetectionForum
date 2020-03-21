package pl.dr.forum.model;

import lombok.Getter;

import java.util.ArrayList;
import java.util.List;

public class Topic {

    @Getter
    private String name;
    private List<Comment> comments;

    public Topic(String name){
        this.name = name;
        this.comments = new ArrayList<>();
    }

    public void addComment(Comment comment){
        this.comments.add(comment);
    }

    public void addComment(String comment){
        this.comments.add(new Comment(comment));
    }
}
