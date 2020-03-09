from .testutils import VerminTest, detect, current_version, visit

class VerminModuleTests(VerminTest):
  def test_return_annotation(self):
    if current_version() >= 3.0:
      self.assertOnlyIn((3, 0), detect("def foo() -> str:\n\treturn ''"))

  def test_arg_annotation(self):
    if current_version() >= 3.0:
      self.assertOnlyIn((3, 0), detect("def foo(bar: int):\n\tpass"))

  def test_var_annotation(self):
    if current_version() >= 3.6:
      self.assertOnlyIn((3, 6), detect("a: int = 5"))

  def test_Final_annotation(self):
    if current_version() >= 3.6:
      self.assertOnlyIn((3, 8), detect("a: Final = 5"))
      self.assertOnlyIn((3, 8), detect("a: Final[int] = 5"))
      self.assertOnlyIn((3, 8), detect("a: typing.Final[int] = 5"))

  def test_Literal_annotation(self):
    if current_version() >= 3.6:
      visitor = visit("a: Literal = 5")
      self.assertTrue(visitor.literal_annotations())
      self.assertOnlyIn((3, 8), visitor.minimum_versions())

      visitor = visit("a: Literal[int] = 5")
      self.assertTrue(visitor.literal_annotations())
      self.assertOnlyIn((3, 8), visitor.minimum_versions())

      visitor = visit("def only_four(x: Literal[4]):\n\treturn x")
      self.assertTrue(visitor.literal_annotations())
      self.assertOnlyIn((3, 8), visitor.minimum_versions())

      visitor = visit("def foo(x: typing.Literal[4]):\n\treturn x")
      self.assertTrue(visitor.literal_annotations())
      self.assertOnlyIn((3, 8), visitor.minimum_versions())
