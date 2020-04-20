package pl.dr.forum.model;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.*;

@NoArgsConstructor
@Entity
public class Comment {

    public static final int HATE_SPEECH_COUNTER_LIMIT = 10;

    @Id
    @GeneratedValue
    @Getter
    private int id;
    @Getter
    @Setter
    private String content;
    @Getter
    @Setter
    @ManyToOne(fetch = FetchType.LAZY)
    private Topic topic;
    @Getter
    @Setter
    private int hateSpeechCount;
    @Getter
    @Setter
    private boolean hateSpeech;

    public Comment(String comment) {
        this.content = comment;
        //TODO check if hate speech
    }
}
