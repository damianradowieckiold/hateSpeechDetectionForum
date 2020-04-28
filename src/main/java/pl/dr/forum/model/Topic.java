package pl.dr.forum.model;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.*;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import java.util.ArrayList;
import java.util.List;

@NoArgsConstructor
@Entity
public class Topic {

    @Id
    @GeneratedValue
    @Getter
    @Setter
    private int id;
    @Getter
    @Setter
    @NotNull(message = "Nazwa nie może być pusta")
    @Size(min = 2, message = "Nazwa musi być służsza niż 2 znaki.")
    private String name;
    @Getter
    @Setter
    @OneToMany(mappedBy = "topic", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Comment> comments;

    public Topic(String name){
        this.name = name;
        this.comments = new ArrayList<>();
    }

    public void addComment(Comment comment){
        this.comments.add(comment);
    }

}
