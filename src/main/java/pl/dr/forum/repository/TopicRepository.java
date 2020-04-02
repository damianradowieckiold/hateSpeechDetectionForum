package pl.dr.forum.repository;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;
import pl.dr.forum.model.Topic;

@Repository
public interface TopicRepository extends CrudRepository<Topic, Integer> {

}
