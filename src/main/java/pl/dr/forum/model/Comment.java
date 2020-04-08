package pl.dr.forum.model;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.*;

@NoArgsConstructor
@Entity
public class Comment {
    @Id
    @GeneratedValue
    @Getter
    private int id;
    @Getter
    @Setter
    private String content;
    @Getter
    @ManyToOne(fetch = FetchType.LAZY)
    private Topic topic;

    public Comment(String comment) {
        this.content = comment;
    }
}
