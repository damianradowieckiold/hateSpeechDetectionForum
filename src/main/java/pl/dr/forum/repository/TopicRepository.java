package pl.dr.forum.repository;

import org.springframework.stereotype.Repository;
import pl.dr.forum.model.Topic;

import java.util.ArrayList;
import java.util.List;

@Repository
public class TopicRepository {

    private static List<Topic> topics;

    {
        topics = new ArrayList<>();
        Topic a = new Topic("O ptakach");
        a.addComment("Ptaki fruwaja po lace");
        a.addComment("Popierdoleni ekolodzy!!!");
        Topic b = new Topic("O drzewach");
        b.addComment("Przywiązać ich do drzew");
        b.addComment("Szumią drzewa");

        topics.add(a);
        topics.add(b);
    }

    public List<Topic> getAll(){
        return topics;
    }
}
