package pl.dr.forum.repository;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;
import pl.dr.forum.model.Comment;

@Repository
public interface CommentRepository extends CrudRepository<Comment, Integer> {

}
