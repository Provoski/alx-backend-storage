-- creates a trigger that decreases the quantity
-- of an item after adding a new order
DELIMITER //

CREATE TRIGGER after_insert_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    -- Update the quantity in the items table
    UPDATE items
    SET quantity = GREATEST((SELECT quantity FROM items WHERE item_id = NEW.item_id) - NEW.quantity, -999999)
    WHERE item_id = NEW.item_id;
END;

//

DELIMITER ;
