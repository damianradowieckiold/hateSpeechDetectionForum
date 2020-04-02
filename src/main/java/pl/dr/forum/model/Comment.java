package pl.dr.forum.model;

import lombok.Getter;
import lombok.NoArgsConstructor;

import javax.persistence.*;

@NoArgsConstructor
@Entity
public class Comment {
    @Id
    @GeneratedValue
    private int id;
    @Getter
    private String content;
    @Getter
    @ManyToOne(fetch = FetchType.LAZY)
    private Topic topic;

    public Comment(String comment) {
        this.content = comment;
    }
}
