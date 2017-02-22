import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.http.*;
import java.nio.charset.Charset;

public class Hello extends HttpServlet {
  @Override
  protected void doGet(HttpServletRequest req, HttpServletResponse resp)
      throws ServletException, IOException {
    resp.getWriter().print("Hello World");
  }
}
