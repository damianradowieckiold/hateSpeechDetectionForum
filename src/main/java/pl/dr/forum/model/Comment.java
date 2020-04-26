package pl.dr.forum.model;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.*;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

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
    @NotNull(message = "Treść nie może być pusta")
    @Size(min = 2, message = "Treść musi być służsza niż 2 znaki.")
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
    }
}
