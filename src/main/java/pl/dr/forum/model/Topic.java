package pl.dr.forum.model;

import lombok.Getter;
import lombok.NoArgsConstructor;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.OneToMany;
import java.util.ArrayList;
import java.util.List;

@NoArgsConstructor
@Entity
public class Topic {

    @Id
    @GeneratedValue
    @Getter
    private int id;
    @Getter
    private String name;
    @OneToMany(mappedBy = "topic")
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

    public List<Comment> getComments() {
        return this.comments;
    }
}
